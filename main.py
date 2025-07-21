import os
import json
import asyncio
from pathlib import Path
from typing import Type, Dict, Any, Literal, Set, Optional, Union

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Local Module Imports ---
# (Assuming these models are defined as in your original code)
from models.classificationModel import SimpleClassification, DocumentType
from models.resumeModel import Resume
from models.citationModel import CitationFile
from models.githubActionModel import GitHubAction, RunsJavascript, RunsComposite, RunsDocker

# Import the newly created async utility functions
from utils.textExtraction import read_file_from_memory_async
from utils.inference import run_inference_async

load_dotenv()

# --- Application Setup ---
app = FastAPI(
    title="Unstructured Text to JSON API v2",
    description="An improved system to convert large unstructured documents into a structured JSON format using a map-and-merge strategy."
)

# --- Configuration & Constants ---
MODEL_NAME = "llama-3.3-70b-versatile" #os.getenv("MODEL_NAME", "llama3-8b-8192") # Using a Groq model name
PROMPT_DIR = "prompts"
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 200

# --- Helper Classes & Registries ---

class PromptManager:
    """Handles loading and preparing prompt templates."""
    def __init__(self, prompt_dir: str):
        self.prompt_dir = Path(prompt_dir)
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, str]:
        templates = {}
        for f in self.prompt_dir.glob("*.prompt"):
            templates[f.stem] = f.read_text(encoding="utf-8")
        for f in self.prompt_dir.glob("*.rules"):
            templates[f.stem] = f.read_text(encoding="utf-8")
        return templates

    # --- CORRECTED METHOD SIGNATURE ---
    # 'variables' is now a required positional argument again, and
    # 'doc_type' is an optional keyword argument.
    def get_prepared_prompt(
        self, name: str, model: Type[BaseModel], variables: Dict[str, Any], doc_type: Optional[DocumentType] = None
    ) -> str:
        template = self.prompts.get(name)
        if not template:
            raise ValueError(f"Prompt '{name}' not found.")

        # --- CORRECTED LOGIC: Only look for rules if doc_type is provided ---
        schema_rules = ""
        if doc_type:
            schema_rules = self.prompts.get(doc_type.value.lower(), "")

        schema = json.dumps(model.model_json_schema(), indent=2)

        all_vars = {
            "pydantic_schema_json": schema,
            "schema_specific_rules": schema_rules,
            **variables
        }

        for key, value in all_vars.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
        return template

prompt_manager = PromptManager(PROMPT_DIR)

class SchemaMetadata(BaseModel):
    model: Type[BaseModel]
    complexity: Literal["low", "medium", "high"]

SCHEMA_REGISTRY: Dict[DocumentType, SchemaMetadata] = {
    DocumentType.RESUME: SchemaMetadata(model=Resume, complexity="medium"),
    DocumentType.CITATION: SchemaMetadata(model=CitationFile, complexity="high"),
    DocumentType.README: SchemaMetadata(model=GitHubAction, complexity="medium"),
}

def _deep_merge_dicts(source: dict, destination: dict) -> dict:
    """Recursively merges source dict into destination dict."""
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            _deep_merge_dicts(value, node)
        elif isinstance(value, list):
            if key not in destination or not isinstance(destination.get(key), list):
                destination[key] = []
            # Avoid duplicates in lists of strings/numbers
            if all(isinstance(item, (str, int, float)) for item in value):
                 destination[key].extend([v for v in value if v not in destination[key]])
            else: # For lists of objects, append all
                 destination[key].extend(value)
        else:
            if key not in destination: # Only set if not already present
                destination[key] = value
    return destination

# In main.py

class DocumentProcessor:
    """
    Encapsulates the logic for processing a document using a robust
    Map -> Merge -> Validate -> Correct strategy.
    """
    def __init__(self, content: str):
        self.content = content
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    async def run_async(self) -> Dict[str, Any]:
        """
        Main orchestration method that processes, validates, and corrects the data.
        """
        # --- Step 1: Classification ---
        print("--- Step 1: Classification ---")
        first_chunk = self.content[:CHUNK_SIZE]
        classification_result = await self._classify_document_async(first_chunk)
        doc_type = classification_result.type
        print(f"   -> Classified as: {doc_type.value}")

        if doc_type == DocumentType.OTHER:
            raise HTTPException(status_code=400, detail="Document type could not be determined.")

        metadata = SCHEMA_REGISTRY.get(doc_type)
        if not metadata:
            raise HTTPException(status_code=404, detail=f"No extraction schema for type: '{doc_type.value}'")

        # --- Step 2: Map & Merge All Chunks ---
        print("--- Step 2: Extracting and Merging All Chunks ---")
        chunks = self.text_splitter.split_text(self.content)
        print(f"   -> Document split into {len(chunks)} chunks.")

        final_extracted_data = {}
        extracted_keys: Set[str] = set()

        for i, chunk in enumerate(chunks):
            print(f"   -> Processing chunk {i+1}/{len(chunks)}...")
            partial_data = await self._extract_from_chunk_async(chunk, doc_type, metadata.model, extracted_keys)
            if partial_data:
                final_extracted_data = _deep_merge_dicts(partial_data, final_extracted_data)
                newly_found_keys = {k for k, v in partial_data.items() if v is not None}
                extracted_keys.update(newly_found_keys)
                print(f"      -> Found keys: {newly_found_keys}")

        # --- Step 3 & 4: Validate and Correct ---
        try:
            print("--- Step 3: Final Validation ---")
            validated_data = metadata.model.model_validate(final_extracted_data)
            print("   -> Validation successful on the first attempt.")
            return {"classification": classification_result, "structured_data": validated_data}

        except ValidationError as e:
            print("\n--- Step 4: Validation Failed. Initiating Correction Pass ---")
            print(f"   -> Validation Errors: {e}")

            correction_prompt = prompt_manager.get_prepared_prompt(
                "correction",
                metadata.model,
                variables={
                    "invalid_json": json.dumps(final_extracted_data, indent=2),
                    "validation_errors": str(e)
                },
                doc_type=doc_type
            )
            
            print("   -> Sending data to LLM for correction...")
            corrected_json_str = await run_inference_async(correction_prompt, MODEL_NAME)
            
            try:
                corrected_data = json.loads(corrected_json_str)
                print("   -> Re-validating the corrected JSON...")
                validated_data = metadata.model.model_validate(corrected_data)
                print("   -> Correction and re-validation successful!")
                return {"classification": classification_result, "structured_data": validated_data}
            except (json.JSONDecodeError, ValidationError) as final_error:
                print(f"   -> FATAL: Correction pass failed to produce valid JSON. Error: {final_error}")
                raise HTTPException(
                    status_code=422, # Unprocessable Entity
                    detail=f"The model could not correct its own validation errors. Last error: {final_error}"
                )

    async def _classify_document_async(self, content_chunk: str) -> SimpleClassification:
        """Helper to classify the document type from the first chunk."""
        prompt = prompt_manager.get_prepared_prompt(
            "classification",
            SimpleClassification,
            {"document_content": content_chunk}
        )
        classification_json = await run_inference_async(prompt, MODEL_NAME)
        return SimpleClassification.model_validate_json(classification_json)

    async def _extract_from_chunk_async(
        self, chunk: str, doc_type: DocumentType, model: Type[BaseModel], extracted_keys: Set[str]
    ) -> Dict[str, Any]:
        """Helper to extract data from a single chunk (the "Map" step)."""
        all_schema_keys = set(model.model_fields.keys())
        missing_keys = all_schema_keys - extracted_keys

        prompt = prompt_manager.get_prepared_prompt(
            "extraction_stateful",
            model,
            variables={
                "document_content": chunk,
                "document_type": doc_type.value,
                "extracted_keys": ", ".join(sorted(list(extracted_keys))) or "None",
                "missing_keys": ", ".join(sorted(list(missing_keys)))
            },
            doc_type=doc_type
        )
        extraction_json = await run_inference_async(prompt, MODEL_NAME)
        try:
            return json.loads(extraction_json)
        except json.JSONDecodeError:
            print(f"      -> Warning: LLM produced invalid JSON for a chunk. Skipping.")
            return {}
        
# --- API Endpoint ---
@app.post("/process_document_v2/", summary="Upload and process a large document asynchronously")
async def process_document_v2(file: UploadFile = File(...)):
    """
    Handles large document processing by:
    1. Reading the file into memory asynchronously.
    2. Using a DocumentProcessor to orchestrate classification and chunked extraction.
    3. Returning the final, merged, and validated structured data.
    """
    _, file_ext = os.path.splitext(file.filename)

    try:
        file_bytes = await file.read()
        content = await read_file_from_memory_async(file_bytes, file_ext)

        processor = DocumentProcessor(content)
        result = await processor.run_async()
        
        return result

    except HTTPException as http_exc:
        raise http_exc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred while processing the file.")