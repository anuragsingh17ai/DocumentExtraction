import os
from openai import AsyncOpenAI # Import the asynchronous client
from dotenv import load_dotenv
load_dotenv()

def get_async_llm_client():
    """Initializes and returns the Asynchronous OpenAI client."""
    # Using GROQ as per your original code
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    return AsyncOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


async def run_inference_async(prompt: str, model_name: str) -> str:
    """
    Runs a prompt against the specified model asynchronously using AsyncOpenAI.
    Instructs the model to return a JSON object.
    """
    client = get_async_llm_client()
    print(f"Running async inference with model: {model_name}...")
    try:
        # Use 'await' for the non-blocking API call
        response = await client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Received an empty response from the model.")
        return content
    except Exception as e:
        print(f"An error occurred during OpenAI API call: {e}")
        raise