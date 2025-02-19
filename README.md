# Cover Letter Generator

## Overview
The **Cover Letter Generator** is a web application designed to generate personalized cover letters based on an uploaded resume and a job description link. The project utilizes **FastAPI** for the backend, **Hugging Face** and **LangChain** for natural language processing (LLM-based cover letter generation), and a simple **HTML, CSS, and JavaScript** frontend.

## Features
- Upload your resume (PDF or text format)
- Provide a job description link
- Automatically generate a tailored cover letter using AI
- Download the generated cover letter for job applications

## Tech Stack
### Backend
- **FastAPI**: A modern, fast (high-performance) web framework for Python
- **Hugging Face Transformers**: For utilizing powerful language models (LLM)
- **LangChain**: Enhances LLMs to generate structured and meaningful cover letters
- **Render (Free Version)**: Used for deploying the backend server

### Frontend
- **HTML, CSS**: Provides the structure and styling for the web interface
- **JavaScript (script.js)**: Handles frontend logic and interacts with the backend API

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python (>= 3.8)
- Node.js (if needed for frontend development)
- Virtual environment (recommended)

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cover-letter-generator.git
   cd cover-letter-generator
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Open the `index.html` file in a browser or use a simple HTTP server:
   ```bash
   python -m http.server 8000  # If needed
   ```

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST   | `/generate` | Upload resume and job link to generate cover letter |
| GET    | `/health` | Check API status |

## Usage
1. Open the web application in a browser.
2. Upload your resume file.
3. Paste the job description link.
4. Click "Generate Cover Letter" to receive a customized cover letter.
5. Download the generated document.

# Block Diagram


![image](https://github.com/user-attachments/assets/8d0a3fb2-3580-478a-af66-c0760aecf3bb)



User submits resume & job link → Sent via JavaScript.
JavaScript makes an API request to the FastAPI backend (Render).
Backend processes the data using Hugging Face & LangChain.
Generated cover letter is returned to the frontend.

## Future Improvements
- Add user authentication for saving generated cover letters
- Implement a database for storing resumes and past cover letters
- Improve LLM prompts for better customization

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss the improvements.

## License
Feel free to modify the code based on your project's specific details! or provide suggestions to improve the code . 
!! Open for suggestions 

