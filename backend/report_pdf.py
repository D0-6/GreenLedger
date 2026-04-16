import os
import asyncio
import hashlib
from jinja2 import Template
from playwright.async_api import async_playwright
import datetime
import base64

# LaTeX-Style HTML Template with 9-Point Institutional Structure
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;700&display=swap');
        
        @page {
            margin: 0;
            size: A4;
        }

        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            margin: 0;
            padding: 0;
            background: white;
        }
        
        .page {
            width: 210mm;
            min-height: 297mm;
            padding: 25mm;
            box-sizing: border-box;
            position: relative;
            overflow: hidden; /* For corner graphics */
        }

        /* 1. COVER PAGE: NEW GREEN STYLE ADAPTATION */
        .cover-page {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            text-align: left;
            page-break-after: always;
            background: #fff;
        }

        .cover-corner-top {
            position: absolute;
            top: -50px;
            right: -50px;
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #a7d08c 0%, #3d7a36 100%);
            clip-path: polygon(100% 0, 0 0, 100% 100%);
            z-index: 0;
        }

        .cover-corner-bottom {
            position: absolute;
            bottom: -50px;
            left: -50px;
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #3d7a36 0%, #a7d08c 100%);
            clip-path: polygon(0 0, 0 100%, 100% 100%);
            z-index: 0;
        }

        .cover-logo {
            font-weight: 900;
            font-size: 72px; /* Large institutional logo */
            color: #3d7a36;
            margin-bottom: 20px;
            z-index: 1;
        }

        .cover-title {
            font-weight: 900;
            font-size: 28px;
            color: #000;
            margin-bottom: 60px;
            z-index: 1;
        }

        .cover-meta {
            font-size: 14px;
            color: #3d7a36;
            line-height: 2;
            z-index: 1;
        }

        .cover-meta b { font-weight: 700; }

        h2 {
            font-size: 14px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-left: 4px solid #3d7a36;
            padding-left: 15px;
            margin-top: 40px;
            margin-bottom: 15px;
        }

        .exec-summary {
            font-family: 'Libre Baskerville', serif;
            font-size: 16px;
            background: #fbfdfb;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            font-style: italic;
            border: 1px solid #e1eedd;
        }

        .risk-container {
            display: flex;
            align-items: center;
            gap: 40px;
            margin-bottom: 40px;
            background: #fff;
            padding: 20px;
            border: 1px solid #eee;
            border-radius: 8px;
        }

        .risk-gauge {
            width: 150px;
            height: 150px;
        }

        .risk-text {
            flex: 1;
        }

        .risk-score-large {
            font-size: 48px;
            font-weight: 900;
            margin: 0;
        }

        .verdict-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 900;
            font-size: 10px;
            text-transform: uppercase;
            margin-top: 10px;
        }

        .badge-REJECTED { background: #fee2e2; color: #991b1b; }
        .badge-ACCEPTED { background: #dcfce7; color: #166534; }
        .badge-SUBSTANTIATED { background: #fef3c7; color: #92400e; }

        .matrix-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            font-size: 11px;
        }

        .matrix-table th {
            text-align: left;
            padding: 10px;
            background: #000;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .matrix-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }

        .status-pill {
            font-weight: 900;
            font-size: 8px;
            padding: 2px 6px;
            border-radius: 3px;
        }

        .status-PASS { background: #dcfce7; color: #166534; }
        .status-FAIL { background: #fee2e2; color: #991b1b; }

        .evidence-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 11px;
        }

        .evidence-table th { background: #f0f0f0; padding: 10px; text-align: left; }
        .evidence-table td { padding: 10px; border-bottom: 1px solid #eee; }

        .screenshot-grid {
            page-break-before: always;
            padding: 25mm;
        }

        .screenshot-item {
            margin-bottom: 40px;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
        }

        .screenshot-img {
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .hash-footer {
            margin-top: 60px;
            padding: 20px;
            background: #f8f8f8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9px;
            text-align: center;
            border-radius: 4px;
        }

        .ledger-hash {
            font-weight: 700;
            color: #000;
            margin-top: 5px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <!-- 1. COVER PAGE: REPLICATING USER TEMPLATE -->
    <div class="page cover-page">
        <div class="cover-corner-top"></div>
        <div class="cover-corner-bottom"></div>
        
        <div class="cover-logo">Greenledger</div>
        <div class="cover-title">{{ claim_text }}</div>
        
        <div class="cover-meta">
            Prepared by: <b>GreenLedger</b><br>
            Date of Report Generation: <b>{{ timestamp }}</b><br>
            Report Code: <b>{{ signature }}</b>
        </div>
    </div>

    <!-- 2. EXECUTIVE SUMMARY -->
    <div class="page">
        <div class="cover-corner-top" style="opacity: 0.1; width: 200px; height: 200px;"></div>
        <h2>Executive Summary</h2>
        <div class="exec-summary">
            {{ exec_summary | safe }}
        </div>

        <!-- 3. RISK SCORE (CHART) -->
        <h2>Risk Score Analysis</h2>
        <div class="risk-container">
            <div class="risk-gauge">
                <svg viewBox="0 0 100 50">
                    <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#eee" stroke-width="12" />
                    <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="{{ 'red' if risk_score > 70 else ('orange' if risk_score > 30 else 'green') }}" stroke-width="12" stroke-dasharray="{{ risk_score * 1.256 }}, 125.6" />
                </svg>
            </div>
            <div class="risk-text">
                <div class="risk-score-large">{{ risk_score }}/100</div>
                <div class="verdict-badge badge-{{ verdict_class }}">{{ verdict }}</div>
                <p style="font-size: 11px; color: #666; margin-top: 10px;">
                    This score reflects the calculated delta between telemetry search verification and self-reported performance.
                </p>
            </div>
        </div>

        <!-- 4. CLAIM -->
        <h2>Claim Profile</h2>
        <div style="font-family: 'Libre Baskerville', serif; font-size: 18px; margin-bottom: 30px;">
            "{{ claim_text }}"
        </div>

        <!-- 5. KEY ISSUES -->
        <h2>Key Forensic Issues</h2>
        <div style="font-size: 13px;">
            {{ key_issues | safe }}
        </div>

        <!-- 6. EVIDENCE TABLE -->
        <h2>Evidence Exhibit Matrix</h2>
        <table class="matrix-table">
            <thead>
                <tr>
                    <th>Benchmark</th>
                    <th>Status</th>
                    <th>Forensic Note</th>
                </tr>
            </thead>
            <tbody>
                {% for row in matrix %}
                <tr>
                    <td>{{ row.criterion }}</td>
                    <td><span class="status-pill status-{{ row.status }}">{{ row.status }}</span></td>
                    <td>{{ row.reason }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- 8. CONCLUSION -->
        <h2>Institutional Conclusion</h2>
        <div class="explanation">
            {{ conclusion | safe }}
        </div>

        <!-- 9. LEDGER HASH -->
        <div class="hash-footer">
            INSTITUTIONAL AUDIT LEDGER HASH (DIGITAL SIGNATURE)
            <div class="ledger-hash">{{ signature }}</div>
            <div style="margin-top: 10px; color: #999;">
                This hash serves as an immutable forensic anchor for the GreenLedger protocol.
            </div>
        </div>
    </div>

    <!-- 7. SCREENSHOTS -->
    <div class="screenshot-grid">
        <h2>Source Evidence Appendix</h2>
        {% for img in screenshots %}
        <div class="screenshot-item">
            <div style="font-size: 10px; font-weight: 900; text-transform: uppercase;">Exhibit {{ loop.index }}: {{ img.title }}</div>
            <div style="font-size: 9px; color: #666; margin-bottom: 5px;">Source: {{ img.url }}</div>
            <img class="screenshot-img" src="data:image/png;base64,{{ img.base64 }}">
        </div>
        {% endfor %}
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
            conclusion = conclusion.replace("\n\n", "</p><p>")
            conclusion = f"<p>{conclusion}</p>"

        if "Key Issues:" in analysis_text:
            issues = analysis_text.split("Key Issues:")[1].split("**")[0].strip().split("\n")
            key_issues = "<ul>" + "".join([f"<li>{i.replace('-', '').strip()}</li>" for i in issues if i.strip()]) + "</ul>"

        if "Forensic Credibility Matrix:" in analysis_text:
            parts = analysis_text.split("Forensic Credibility Matrix:")[1].split("**")[0].strip().split("\n")
            for line in parts:
                if ":" in line and "-" in line:
                    crit = line.split(":")[0].replace("-", "").strip()
                    status_reason = line.split(":")[1].strip()
                    status = "PASS" if "PASS" in status_reason.upper() else "FAIL"
                    reason = status_reason.split("-")[1].strip() if "-" in status_reason else status_reason
                    matrix.append({"criterion": crit, "status": status, "reason": reason})

    except Exception as e:
        print(f"Institutional Parsing Error: {e}")
        
    return matrix, exec_summary, conclusion, key_issues

async def generate_institutional_pdf(audit_data: dict, screenshots: list):
    matrix, exec_summary, conclusion, key_issues = parse_forensic_data(audit_data['analysis'])
    
    encoded_screenshots = []
    for s in screenshots:
        if os.path.exists(s['path']):
            with open(s['path'], "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode('utf-8')
                encoded_screenshots.append({
                    "title": s['title'],
                    "url": s['url'],
                    "base64": encoded
                })

    template_data = {
        "report_id": f"GL-{datetime.datetime.now().strftime('%Y%j%H%M')}",
        "timestamp": datetime.datetime.now().strftime("%B %d, %Y | %H:%M UTC"),
        "claim_text": audit_data.get('claim_text', 'Technical ESG Statement'),
        "verdict": audit_data.get('verdict', 'SUBSTANTIATED RISK'),
        "verdict_class": audit_data.get('verdict', 'SUBSTANTIATED').split()[0],
        "risk_score": audit_data.get('risk_score', 50),
        "matrix": matrix,
        "exec_summary": exec_summary,
        "conclusion": conclusion,
        "key_issues": key_issues,
        "screenshots": encoded_screenshots,
        "signature": hashlib.sha256(audit_data.get('analysis', '').encode()).hexdigest().upper()
    }

    template = Template(HTML_TEMPLATE)
    html_content = template.render(**template_data)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_content(html_content)
        
        pdf_path = f"backend/reports/audit_{template_data['report_id']}.pdf"
        os.makedirs("backend/reports", exist_ok=True)
        
        await page.pdf(path=pdf_path, format="A4", print_background=True)
        await browser.close()
        return pdf_path
