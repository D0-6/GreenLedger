import os
import json
import asyncio
import hashlib
from openai import AsyncOpenAI
from duckduckgo_search import DDGS
from dotenv import load_dotenv

load_dotenv()

# NVIDIA NIM Configuration (Llama 3.1)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)
LLM_MODEL = "meta/llama-3.1-70b-instruct"

def generate_optimized_queries(claim: str):
    return [
        f"{claim} 2025 OR 2026",
        f"{claim} greenwashing OR emissions increased OR Scope 3 missing OR regulatory fine 2025 OR 2026",
        f"{claim} CSRD OR SEC climate disclosure 2026"
    ]

def live_search_sync(query: str, max_results=4):
    try:
        # DDGS sometimes needs higher timeouts in serverless environments
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        print(f"Search failed for query '{query}': {e}")
        return []

async def analyze_claim_stream(claim: str, pdf_text: str = None):
    """Async Generator version optimized for Vercel 10s timeouts."""
    try:
        # 1. IMMEDIATE HEARTBEAT (Resets Vercel timeout)
        yield json.dumps({"type": "trace", "message": f"Establishing secure G7 telemetry tunnel ({provider_name})..."}) + "\n"
        await asyncio.sleep(0.05)

        if not NVIDIA_API_KEY:
            yield json.dumps({"type": "error", "message": "Forensic telemetry lost: NVIDIA_API_KEY missing in Vercel Dashboard."}) + "\n"
            return
        
        # 2. HEARTBEAT PULSE
        yield json.dumps({"type": "trace", "message": "Synchronizing forensic nodes..."}) + "\n"

        # If PDF text is provided, use it for context
        eff_claim = claim
        if pdf_text and len(claim) < 10:
            eff_claim = f"Verification of report content: {pdf_text[:100]}"
            yield json.dumps({"type": "trace", "message": "PDF content detected. Extracting forensic anchors..."}) + "\n"

        queries = generate_optimized_queries(eff_claim)
        
        # 3. PARALLEL SEARCH (Parallel is 3x faster than sequential)
        yield json.dumps({"type": "trace", "message": "Engaging parallel telemetry sweep..."}) + "\n"
        
        async def fetch_one(q):
            return await asyncio.to_thread(live_search_sync, q)

        # Run all searches concurrently to beat the 10s clock
        search_tasks = [fetch_one(q) for q in queries]
        search_results_lists = await asyncio.gather(*search_tasks)
        
        all_results = []
        for i, results in enumerate(search_results_lists):
            query = queries[i]
            for r in results[:2]:
                title = r.get('title', 'Unknown Source')
                url = r.get('href', 'N/A')
                yield json.dumps({"type": "link", "message": f"Inspecting: {title}", "url": url}) + "\n"
            all_results.extend(results)

        context = "\n".join([f"Title: {r.get('title')}\nSnippet: {r.get('body') or r.get('snippet') or r.get('href')}" 
                           for r in all_results[:10]])
        if pdf_text:
            context = f"PRIMARY DOCUMENT CONTENT:\n{pdf_text[:3000]}\n\nLIVE SEARCH TELEMETRY:\n{context}"
        
        yield json.dumps({"type": "trace", "message": "Sweep complete. Synthesizing results..."}) + "\n"
    except Exception as e:
        yield json.dumps({"type": "error", "message": f"Telemetry drop: {str(e)}"}) + "\n"
        context = "Live search unavailable."

    # Institutional 9-Point Prompt
    prompt = f"""
You are GreenLedger AI, a lead forensic ESG auditor with 15+ years of experience in corporate sustainability compliance (CSRD, ISSB, SEC). 

STRICT OUTPUT FORMAT (9-Point Audit Structure):
**Risk Score:** [0-100]/100
**Forensic Verdict:** [REJECTED | ACCEPTED | SUBSTANTIATED RISK]

**Executive Summary:**
[A high-level institutional abstract of the audit finding. No bullets.]

**Claim Summary:**
[Technical description of the statement under audit.]

**Forensic Credibility Matrix:**
- [Criterion]: [PASS|FAIL|PARTIAL] - [Brief reason]
(List 5 items)

**Risk Methodology Breakdown:**
- [Component]: [X]% weighting
(List 3 components)

**Key Issues:**
- [Technical bullet points]

**Explanation:**
[2-3 paragraphs of deep narrative-driven forensic synthesis. Reference sources.]

**Conclusion:**
[Final institutional verdict and technical justification.]

**Evidence Exhibit Logs:**
- [Source Title]: [Findings]

### THE RELAYTO PROTOCOL:
- NO BULLET POINTS in 'Executive Summary', 'Explanation', or 'Conclusion'.
- Maintain a strictly impartial, academic, and authoritative tone.

Analyze:
Claim: {claim}
{"Report Content: " + pdf_text[:2000] if pdf_text else ""}
Context: {context}
"""

    try:
        yield json.dumps({"type": "trace", "message": f"Applying {provider_name} Forensic Synthesis..."}) + "\n"
        
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=1500,
            stream=True
        )
        
        full_text = ""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                full_text += chunk.choices[0].delta.content

        # Robust Parsing
        risk_level = "UNKNOWN"
        risk_score = 50
        verdict = "SUBSTANTIATED RISK"
        
        if "**Risk Score:**" in full_text:
            try:
                score_str = full_text.split("**Risk Score:**")[1].split("/100")[0]
                score_val = "".join(filter(str.isdigit, score_str))
                if score_val:
                    risk_score = int(score_val)
                    if risk_score < 30: risk_level = "LOW"
                    elif risk_score < 70: risk_level = "MEDIUM"
                    else: risk_level = "HIGH"
            except: pass
            
        if "**Forensic Verdict:**" in full_text:
            try:
                v_part = full_text.split("**Forensic Verdict:**")[1].split("\n")[0].strip()
                verdict = v_part.replace("[", "").replace("]", "").strip()
            except: pass

        yield json.dumps({
            "type": "result", 
            "analysis": full_text, 
            "risk_level": risk_level,
            "risk_score": risk_score,
            "verdict": verdict,
            "search_results": all_results
        }) + "\n"
        
    except Exception as e:
        yield json.dumps({"type": "error", "message": f"Synthesis failure: {str(e)}"}) + "\n"
