from report import generate_word_report
import os

# Mock data matching the new Lead Analyst format
mock_claims = [
    {
        "claim": "Test Corp 2030 Carbon Neutrality",
        "analysis": {
            "analysis": """
**Risk Score:** 85/100
**Claim Summary:** Neutral rephrasing of the claim.
**Key Issues:**
- Issue 1
- Issue 2
**Explanation:** 
Detailed forensic analysis here about the risks and gaps.
**Evidence & Proof:**
- Source 1 | 2024 | Snippet
- Source 2 | 2025 | Snippet
**Visual Recommendations for Report:**
- Chart 1
**Overall Verdict:**
This is a high risk claim.
**Suggestions for Replacement / Institutional-Grade Improvement:**
Provide better data.
""",
            "risk_level": "HIGH",
            "risk_score": 85
        }
    }
]

print("Generating mock report...")
bio = generate_word_report(mock_claims)

output_path = "test_institutional_report.docx"
with open(output_path, "wb") as f:
    f.write(bio.read())

print(f"Report saved to {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
