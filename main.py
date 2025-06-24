from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from typing import Optional
import uvicorn

from services.pdf_processor import PDFProcessor
from services.mcq_generator import MCQGenerator
from services.pdf_creator import PDFCreator
from models.schemas import MCQRequest, MCQResponse

app = FastAPI(
    title="MCQ Generator API",
    description="Generate Multiple Choice Questions from PDF documents or topics using Groq API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
pdf_processor = PDFProcessor()
mcq_generator = MCQGenerator()
pdf_creator = PDFCreator()

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("static", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML interface"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/generate-from-pdf", response_model=MCQResponse)
async def generate_mcq_from_pdf(
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    difficulty: str = Form("medium")
):
    """Generate MCQs from uploaded PDF file"""
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from PDF
        text_content = pdf_processor.extract_text(file_path)
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Generate MCQs
        mcqs = await mcq_generator.generate_from_text(
            text_content, 
            num_questions, 
            difficulty
        )
        
        # Create output PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"mcq_output_{timestamp}.pdf"
        output_path = f"outputs/{output_filename}"
        
        pdf_creator.create_mcq_pdf(mcqs, output_path, source=f"PDF: {file.filename}")
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return MCQResponse(
            questions=mcqs,
            download_url=f"/download/{output_filename}",
            total_questions=len(mcqs)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-from-topic", response_model=MCQResponse)
async def generate_mcq_from_topic(request: MCQRequest):
    """Generate MCQs from a given topic"""
    try:
        # Generate MCQs
        mcqs = await mcq_generator.generate_from_topic(
            request.topic,
            request.num_questions,
            request.difficulty,
            request.subtopics
        )
        
        # Create output PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"mcq_topic_{timestamp}.pdf"
        output_path = f"outputs/{output_filename}"
        
        pdf_creator.create_mcq_pdf(mcqs, output_path, source=f"Topic: {request.topic}")
        
        return MCQResponse(
            questions=mcqs,
            download_url=f"/download/{output_filename}",
            total_questions=len(mcqs)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated PDF file"""
    file_path = f"outputs/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)