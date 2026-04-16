from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import io
import pypdf
import datetime

# Import local modules from current api directory
from . import db, ai, models

app = FastAPI(title="GreenLedger Vercel API")

# Enable CORS (Vercel Backend will likely be on same domain as Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Attempt DB init but don't crash if Railway isn't ready
    try:
        db.init_db()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"⚠️ Database initialization skipped: {e}")

@app.get("/api")
def read_root():
    return {"message": "GreenLedger Vercel API is operational"}

@app.post("/api/analyze")
def analyze(request: models.ClaimRequest):
    return StreamingResponse(
        ai.analyze_claim_stream(request.claim, request.pdf_text),
        media_type="text/event-stream"
    )

@app.post("/api/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        reader = pypdf.PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        return {"text": text, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Extraction failed: {str(e)}")

@app.get("/api/ledger")
def get_ledger():
    return db.get_records()

@app.post("/api/save-to-ledger")
def save_to_ledger(data: dict):
    try:
        db.save_record(data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-report")
async def generate_report(request: models.ReportRequest):
    # PDF generation currently disabled on Vercel due to Playwright size constraints
    # For the hackathon demo, we return a 501 or a text summary
    raise HTTPException(
        status_code=501, 
        detail="Institutional PDF Generation currently disabled in Vercel Serverless mode. Please use Web Dashboard for full results."
    )
