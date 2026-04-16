from report import generate_word_report
import os

# Professional mock data to test the new Relayto layout
mock_claims = [
    {
        "claim": "EcoCorp reaches 100% recycled energy across all G7 data centers.",
        "analysis": {
            "analysis": """
**Risk Score:** 12/100
**Claim Summary:** Verification of energy sourcing across European and North American tier-1 data hubs.
**Key Issues:**
- Minor latency in Scope 2 reporting for newly acquired nodes.
- Regional grid variations in fossil-fuel fallback periods.
**Explanation:** 
Our forensic sweep of renewable energy certificates (RECs) confirms a 98% match with public claims. The remaining 2% represents technical line loss not typically reported in standard disclosures. 
**Evidence & Proof:**
- GridWatch API | 2024 | Real-time verification of PPA agreements at 12 nodes.
- Internal Audit Trace | 2024 | Ledger timestamp match.
**Visual Recommendations for Report:**
- Geographic breakdown of energy mix.
**Overall Verdict:**
AUTHENTIC. High forensic confidence in the energy transition trajectory.
**Suggestions for Replacement / Institutional-Grade Improvement:**
Include regional grid emission factors in the next disclosure cycle to achieve 99% transparency.
""",
            "risk_level": "LOW",
            "risk_score": 12
        }
    }
]

print("Generating high-fidelity Relayto report...")
bio = generate_word_report(mock_claims)

output_path = "Relayto_Audit_V5.docx"
with open(output_path, "wb") as f:
    f.write(bio.read())

print(f"Report saved to {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
