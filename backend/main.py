import os
from fastapi import FastAPI, HTTPException , File, UploadFile, Form
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


app = FastAPI()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

if not HUGGINGFACE_TOKEN:
    raise ValueError("❌ Hugging Face token is missing! Set HUGGINGFACE_TOKEN in environment variables.")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

# Request model
class CoverLetterRequest(BaseModel):
    resume: str
    job_description: str

def query_huggingface(payload):
    """Sends a request to the Hugging Face Inference API and returns the response."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/generate_cover_letter/")
async def generate_cover_letter(request: CoverLetterRequest):
    """Generates a cover letter using the Hugging Face model."""
    try:
        prompt = (
            f"Write a professional cover letter based on this resume:\n{request.resume}\n"
            f"And this job description:\n{request.job_description}\n"
            f"I need the cover letter in paragraph wise\n"
            f"The first paragraph should tell that why the resume person choose to apply for this role\n"
            f"the second , third , fourth paragraph shold tell about how the top three job requiremnets matches your skills\n"
            f"last paragraph is for thanks and asking for interview"
        )

        # Call Hugging Face API
        output = query_huggingface({"inputs": prompt})

        # Extract generated text
        generated_text = output[0]["generated_text"] if isinstance(output, list) else output

        return {"cover_letter": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

