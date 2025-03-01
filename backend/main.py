import os
from fastapi import FastAPI, HTTPException , File, UploadFile, Form
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import fitz

GOOGLE_API_KEY = "AIzaSyDHQ4oxBF3eYLy-vNKbA-U8AwhB2Eivm_E"

# Initialize the Google PaLM (Gemini) model with API key
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY, temperature=0.7)

app = FastAPI()

# Enable CORS for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rithvikns.github.io"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Request model
class CoverLetterRequest(BaseModel):
    resume: str
    job_description: str
    
@app.get("/")
def home():
    return {"message": "Welcome to Resume Cover Letter Generator"}
    
def query_huggingface(payload):
    """Sends a request to the Hugging Face Inference API and returns the response."""
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        try:
            error_detail = response.json()
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text  # In case the error response isn't JSON
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    try:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        else:
            return {"error": "Unexpected response format from Hugging Face API"}
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Invalid response from Hugging Face API")



@app.post("/upload_resume/")

async def upload_resume(resume: UploadFile = File(...)):
    try:
        content = await resume.read()

        if resume.filename.endswith(".pdf"):
            pdf_document = fitz.open(stream=content, filetype="pdf")
            text_content = "\n".join([page.get_text() for page in pdf_document])
        else:
            text_content = content.decode("utf-8", errors="ignore")

        return {"resume_text": text_content}

    except Exception as e:
        return {"error": str(e)}
        
@app.post("/fetch_job_description/")
async def fetch_job_description(url: str = Form(...)):
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        job_description = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

        if not job_description:
            return JSONResponse(status_code=404, content={"detail": "No job description found on the page."})

        return JSONResponse(status_code=200, content={"job_description": job_description})

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"detail": f"Failed to fetch job description: {str(e)}"})



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

        output = llm.invoke(prompt)

        # Extract generated text
        generated_text = output[0]["generated_text"] if isinstance(output, list) else output

        return {"cover_letter": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

