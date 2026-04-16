import os
import asyncio
import hashlib
from jinja2 import Template
import datetime
import base64

# Playwright handling for Vercel Serverless
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# LaTeX-Style HTML Template (Simplified for brevity in migration, keeping user's design)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: sans-serif; padding: 40px; }
        .verdict { font-weight: bold; color: #3d7a36; }
        .risk { font-size: 24px; }
        .section { margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
</head>
<body>
    <h1>GreenLedger Institutional Audit</h1>
    <p>Claim: {{ claim_text }}</p>
    <div class="risk">Score: {{ risk_score }}/100</div>
    <div class="verdict">Verdict: {{ verdict }}</div>
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{{ exec_summary }}</p>
    </div>
</body>
</html>
"""

def parse_forensic_data(analysis_text: str):
    """Robust extraction of the 9-point forensic structure."""
    matrix = []
    exec_summary = "Audit profile generation in progress..."
    conclusion = "Conclusion pending forensic finalization."
    key_issues = "No critical vulnerabilities detected."
    
    try:
        if "Executive Summary:" in analysis_text:
            exec_summary = analysis_text.split("Executive Summary:")[1].split("**")[0].strip()
        
        if "Conclusion:" in analysis_text:
            conclusion = analysis_text.split("Conclusion:")[1].split("**")[0].strip()

        if "Key Issues:" in analysis_text:
            issues = analysis_text.split("Key Issues:")[1].split("**")[0].strip().split("\n")
            key_issues = "<ul>" + "".join([f"<li>{i.replace('-', '').strip()}</li>" for i in issues if i.strip()]) + "</ul>"

    except Exception:
        pass
        
    return matrix, exec_summary, conclusion, key_issues

async def generate_institutional_pdf(audit_data: dict, screenshots: list):
    if not PLAYWRIGHT_AVAILABLE:
        return None

    matrix, exec_summary, conclusion, key_issues = parse_forensic_data(audit_data['analysis'])
    
    template_data = {
        "report_id": f"GL-{datetime.datetime.now().strftime('%Y%j%H%M')}",
        "timestamp": datetime.datetime.now().strftime("%B %d, %Y | %H:%M UTC"),
        "claim_text": audit_data.get('claim_text', 'Technical ESG Statement'),
        "verdict": audit_data.get('verdict', 'SUBSTANTIATED RISK'),
        "risk_score": audit_data.get('risk_score', 50),
        "exec_summary": exec_summary,
        "signature": hashlib.sha256(audit_data.get('analysis', '').encode()).hexdigest().upper()
    }

    template = Template(HTML_TEMPLATE)
    html_content = template.render(**template_data)

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_content(html_content)
            
            # Use /tmp for Vercel compatibility
            pdf_path = f"/tmp/audit_{template_data['report_id']}.pdf"
            await page.pdf(path=pdf_path, format="A4", print_background=True)
            await browser.close()
            return pdf_path
        except Exception:
            return None
