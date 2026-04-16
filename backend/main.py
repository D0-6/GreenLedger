from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import io
import pypdf
import db, ai, models, report, evidence, report_pdf
import datetime

app = FastAPI(title="GreenLedger API")

# Enable CORS for Next.js (Vercel Production & Local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://greenledger.vercel.app", # Placeholder for user's domain
        "*" # Broad allowance for hackathon flexibility; restrictive in prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db():
    db.init_db()

@app.get("/")
def read_root():
    return {"message": "GreenLedger API is operational"}

@app.post("/analyze")
def analyze(request: models.ClaimRequest):
    return StreamingResponse(
        ai.analyze_claim_stream(request.claim, request.pdf_text),
        media_type="text/event-stream"
    )

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

@app.get("/ledger")
def get_ledger():
    return db.get_records()

@app.post("/save-to-ledger")
def save_to_ledger(data: dict):
    try:
        db.save_record(data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-report")
async def generate_report(request: models.ReportRequest):
    try:
        if not request.claims:
            raise HTTPException(status_code=400, detail="No audit data provided")
            
        # Robust selection of the primary audit data
        primary_audit = request.claims[0]
        # In some cases, the frontend might send the analysis directly or wrapped in an 'analysis' key
        audit_body = primary_audit.get('analysis') if isinstance(primary_audit, dict) and 'analysis' in primary_audit else primary_audit

        # Capture Evidence Screenshots
        search_results = audit_body.get('search_results', [])
        screenshot_paths = await evidence.capture_all_evidence(search_results)
        
        exhibits = []
        for i, path in enumerate(screenshot_paths):
            if i < len(search_results):
                exhibits.append({
                    "title": search_results[i].get('title', 'Unknown Source'),
                    "url": search_results[i].get('href', 'N/A'),
                    "path": path
                })
            
        # Generate the Institutional PDF
        pdf_path = await report_pdf.generate_institutional_pdf(audit_body, exhibits)
        
        def iter_file():
            with open(pdf_path, mode="rb") as f:
                yield from f

        return StreamingResponse(
            iter_file(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=GreenLedger_Audit_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"}
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
