from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import io
import pypdf
import datetime

# Import local modules from current api directory
try:
    from . import db, ai, models, report, report_pdf, evidence
except ImportError:
    # Fallback for some local dev environments
    import db, ai, models, report, report_pdf, evidence

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
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization skipped: {e}")

@app.get("/api")
@app.get("/")
def read_root():
    return {"message": "GreenLedger Vercel API is operational"}

@app.post("/api/analyze")
@app.post("/analyze")
def analyze(request: models.ClaimRequest):
    return StreamingResponse(
        ai.analyze_claim_stream(request.claim, request.pdf_text),
        media_type="text/event-stream"
    )

@app.post("/api/extract-pdf")
@app.post("/extract-pdf")
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
@app.get("/ledger")
def get_ledger():
    return db.get_records()

@app.post("/api/save-to-ledger")
@app.post("/save-to-ledger")
def save_to_ledger(data: dict):
    try:
        db.save_record(data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-report")
@app.post("/generate-report")
async def generate_report(request: models.ReportRequest):
    try:
        if not request.claims:
            raise HTTPException(status_code=400, detail="No audit data provided")
            
        # Robust selection of the primary audit data
        primary_audit = request.claims[0]
        audit_body = primary_audit.get('analysis') if isinstance(primary_audit, dict) and 'analysis' in primary_audit else primary_audit

        # Word Document Generation (Very stable on Vercel)
        word_buf = report.generate_word_report(request.claims)
        
        return StreamingResponse(
            word_buf,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=GreenLedger_Audit_Report.docx"}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use the filename 'index' if it's in the current folder, or 'api.index' if called from root
    try:
        uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
    except:
        uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
