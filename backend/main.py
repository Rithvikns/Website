from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import pdfplumber
import requests
from bs4 import BeautifulSoup
import openai

app = FastAPI()

openai.api_key = "your-openai-api-key"

class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/")
def home():
    return {"message": "Welcome to Resume Cover Letter Generator"}

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    else:
        return {"error": "Only PDF files are supported"}
    return {"resume_text": text}

@app.post("/fetch_job_description/")
async def fetch_job_description(url: str = Form(...)):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        job_description = " ".join([p.text for p in paragraphs])
        return {"job_description": job_description}
    else:
        return {"error": "Failed to fetch job description"}

@app.post("/generate_cover_letter/")
async def generate_cover_letter(request: CoverLetterRequest):
    prompt = f"""
    Write a professional cover letter based on the following resume and job description:
    
    Resume: {request.resume_text}
    
    Job Description: {request.job_description}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert cover letter writer."},
                  {"role": "user", "content": prompt}]
    )
    
    cover_letter = response["choices"][0]["message"]["content"]
    return {"cover_letter": cover_letter}
