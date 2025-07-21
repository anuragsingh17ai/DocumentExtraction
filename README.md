# Unstructured Text to JSON API

This project provides a powerful, asynchronous FastAPI application designed to convert unstructured text from various document types (`.pdf`, `.md`, `.bib`, etc.) into a structured JSON format.

The system leverages Large Language Models (LLMs) and a sophisticated processing pipeline to intelligently classify documents, handle files of any size, and ensure the final output strictly adheres to a desired Pydantic schema.

## Key Features

-   **Automatic Document Classification**: Intelligently determines the type of an uploaded document (e.g., Resume, Citation File, GitHub Action) to apply the correct extraction logic.
-   **Multi-File Type Support**: Natively processes PDFs, Markdown files, and BibTeX files (by downloading and parsing the linked PDF).
-   **Large Document Handling**: Uses a text-splitting (chunking) strategy to process documents that are too large to fit in a model's context window.
-   **Stateful Extraction**: A "Map & Merge" pipeline processes chunks sequentially, keeping track of information that has already been extracted to work efficiently.
-   **Schema-Driven Self-Correction**: If the initial merged JSON fails validation against the Pydantic schema, the system performs an automated **Correction Pass**, sending the invalid data and the specific error message back to the LLM to be fixed.
-   **Dynamic & Modular Prompting**: Uses a `PromptManager` to load and prepare prompts. It can inject schema-specific rules (e.g., for GitHub Actions) into a generic template, keeping prompts clean and maintainable.
-   **Fully Asynchronous**: Built with `async/await` from the ground up for high-performance I/O, from file reading to concurrent API calls.

## How It Works: The Processing Pipeline

The application follows a robust "Map -> Merge -> Validate -> Correct" pipeline for each uploaded document.

1.  **Classification**: The first chunk of the document is sent to the LLM to determine its type (e.g., `RESUME`).
2.  **Map & Merge**: The full document is split into overlapping chunks. The system iterates through these chunks, sending each one to the LLM to extract information based on the classified document's Pydantic schema. The results from each chunk are recursively merged into a single JSON object.
3.  **Validate**: The complete merged JSON object is validated against the target Pydantic model. If it's valid, the process succeeds and returns the data.
4.  **Correct**: If validation fails, the system automatically triggers a **Correction Pass**. It sends the invalid JSON, the specific Pydantic `ValidationError` message, and the schema to the LLM with a clear instruction: "Fix this." The newly corrected JSON is then re-validated. This makes the system incredibly resilient to model errors.

## Project Structure

```
.
├── .env                  # Local environment variables (API keys, etc.)
├── main.py               # FastAPI application entrypoint, DocumentProcessor class
├── pyproject.toml        # Project metadata and dependencies for uv
├── models/               # Pydantic models for each document type
│   ├── classificationModel.py
│   ├── resumeModel.py
│   ├── citationModel.py
│   └── githubActionModel.py
├── prompts/              # Prompt templates used by the LLM
│   ├── classification.prompt
│   ├── extraction_stateful.prompt
│   ├── correction.prompt
│   └── github_action.rules   # Example of a schema-specific rule file
└── utils/                # Helper functions for the application
    ├── inference.py
    └── text_extraction.py
```

## Setup and Installation

This project uses **uv** for fast package management and a **.env** file for managing environment variables.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment. `uv` makes this easy.

```bash
# Create a virtual environment named .venv
uv venv

# Activate it (on Windows, use `.venv\Scripts\activate`)
source .venv/bin/activate
```

### 3. Install Dependencies

The project's dependencies are listed in the `pyproject.toml` file. Install them using `uv`.

```bash
# This command reads the dependencies from pyproject.toml and installs them
uv pip install -e .
```

### 4. Create the Environment File

This project requires an API key for the LLM provider (e.g., Groq, OpenAI).

Create a file named `.env` in the root of the project directory. You can copy the example below and fill in your details.

**File: `.env`**
```env
# API key for the LLM provider (using Groq in this example)
GROQ_API_KEY="your_api_key_here"

# The specific model name you want to use
MODEL_NAME="llama3-8b-8192"  # use better model here 
```


## Running the Application

Once the setup is complete, you can run the FastAPI server using `uvicorn`.

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Usage

### Endpoint

`POST /process_document_v2/`

This endpoint accepts a `multipart/form-data` request with a single file.

### Example `curl` Request

Here is an example of how to upload a resume for processing:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/process_document_v2/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@"/path/to/your/resume.pdf"'
```

### Example Success Response

```json
{
  "classification": {
    "type": "RESUME",
    "confidence": 0.95,
    "reasoning": "The document contains sections like 'Education', 'Work Experience', and 'Skills', which are characteristic of a resume."
  },
  "structured_data": {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "phone": "123-456-7890",
    "summary": "A highly motivated software engineer with 5 years of experience...",
    "education": [
      {
        "institution": "State University",
        "degree": "Bachelor of Science",
        "fieldOfStudy": "Computer Science",
        "startDate": "2015",
        "endDate": "2019"
      }
    ],
    "workExperience": [
      // ...
    ]
  }
}
```

## How to Customize and Extend

The system is designed to be easily extensible.

-   **To Add a New Document Type**:
    1.  Create a new Pydantic model in the `models/` directory (e.g., `invoiceModel.py`).
    2.  Add a new `Enum` value to `DocumentType` in `models/classificationModel.py`.
    3.  Add your new model and type to the `SCHEMA_REGISTRY` in `main.py`.
    4.  Update the `classification.prompt` to teach the LLM about this new document type.
-   **To Add Schema-Specific Rules**:
    1.  Create a `.rules` file in the `prompts/` directory named after the `DocumentType` enum value (e.g., `invoice.rules`).
    2.  The `PromptManager` will automatically detect and inject these rules into the extraction prompt whenever that document type is processed.
