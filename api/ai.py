import os
import json
import asyncio
from google import genai
from google.genai import types
from duckduckgo_search import DDGS
from dotenv import load_dotenv

load_dotenv()

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Use Gemini 2.5 Flash for high-speed serverless reasoning
LLM_MODEL = "gemini-2.5-flash"

def generate_optimized_queries(claim: str):
    return [
        f"{claim} 2025 OR 2026",
        f"{claim} greenwashing OR emissions transparency OR regulatory non-compliance 2025",
        f"{claim} CSRD disclosure OR ISSB sustainability standards 2026",
        f"{claim} SEC climate reporting OR ESMA ESG enforcement",
        f"{claim} supply chain forced labor OR scope 3 emissions gaps",
        f"{claim} carbon credits double counting OR offset verification 2025"
    ]

def live_search_sync(query: str, max_results=4):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        print(f"Search failed for query '{query}': {e}")
        return []

async def analyze_claim_stream(claim: str, pdf_text: str = None):
    """Async Generator version optimized for Vercel 10s timeouts."""
    try:
        provider_name = "Google Gemini"
        
        # 1. IMMEDIATE HEARTBEAT (Resets Vercel timeout)
        yield json.dumps({"type": "trace", "message": f"Establishing secure telemetry tunnel ({provider_name})..."}) + "\n"
        await asyncio.sleep(0.05)
        
        # 2. HEARTBEAT PULSE
        yield json.dumps({"type": "trace", "message": "Synchronizing forensic nodes..."}) + "\n"

        eff_claim = claim
        if pdf_text and len(claim) < 10:
            eff_claim = f"Verification of report content: {pdf_text[:100]}"
            yield json.dumps({"type": "trace", "message": "PDF content detected. Extracting forensic anchors..."}) + "\n"

        queries = generate_optimized_queries(eff_claim)
        
        # 3. PARALLEL SEARCH
        yield json.dumps({"type": "trace", "message": "Engaging parallel telemetry sweep..."}) + "\n"
        
        async def fetch_one(q):
            return await asyncio.to_thread(live_search_sync, q)

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

    # Gemini-Optimized Prompt System
    system_instruction = """
    You are GreenLedger AI, a lead forensic ESG auditor with 15+ years of experience in corporate sustainability compliance (CSRD, ISSB, SEC). 
    Your role is to detect greenwashing, assess regulatory gaps, and provide a definitive risk score.
    Maintain a strictly impartial, academic, and authoritative tone. No markdown bullet points in the abstract/summary sections.
    """
    
    prompt = f"""
    Analyze the following ESG claim against the provided telemetry data.
    
    <input_claim>
    {claim}
    </input_claim>
    
    {"<pdf_report>\n" + pdf_text[:2000] + "\n</pdf_report>\n" if pdf_text else ""}
    
    <telemetry_context>
    {context}
    </telemetry_context>

    STRICT OUTPUT FORMAT REQUIRED. You MUST format your response EXACTLY like this template:

    **Risk Score:** [0-100]/100
    **Forensic Verdict:** [REJECTED | ACCEPTED | SUBSTANTIATED RISK]

    **Executive Summary:**
    [A high-level institutional abstract of the audit finding. No bullets.]

    **Claim Summary:**
    [Technical description of the statement under audit.]

    **Forensic Credibility Matrix:**
    - [Criterion 1]: [PASS|FAIL|PARTIAL] - [Brief reason]
    - [Criterion 2]: [PASS|FAIL|PARTIAL] - [Brief reason]
    - [Criterion 3]: [PASS|FAIL|PARTIAL] - [Brief reason]
    - [Criterion 4]: [PASS|FAIL|PARTIAL] - [Brief reason]
    - [Criterion 5]: [PASS|FAIL|PARTIAL] - [Brief reason]

    **Risk Methodology Breakdown:**
    - [Component 1]: [X]% weighting
    - [Component 2]: [Y]% weighting
    - [Component 3]: [Z]% weighting

    **Key Issues:**
    - [Technical bullet point 1]
    - [Technical bullet point 2]
    - [Technical bullet point 3]

    **Explanation:**
    [2-3 paragraphs of deep narrative-driven forensic synthesis. Reference the telemetry context.]

    **Conclusion:**
    [Final institutional verdict and technical justification.]

    **Verification Traceability Map:**
    - [Claim Point]: [Exhibit Title] (Direct anchor to telemetry)

    **Regulatory Compliance Gap Analysis:**
    - [Standard/Article]: [Identification of specific discrepancy or alignment]
    - [Standard/Article]: [Identification of specific discrepancy or alignment]

    **Institutional Challenge Inquiries:**
    - [Technical Question]: [The underlying data discrepancy that prompts this question]

    **Forensic Confidence Score:** [Low|Medium|High] - [X]% based on telemetry density.
    """

    try:
        yield json.dumps({"type": "trace", "message": f"Applying {provider_name} Forensic Synthesis..."}) + "\n"
        
        # Stream response from Gemini using aio
        response_stream = client.aio.models.generate_content_stream(
            model=LLM_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,
                max_output_tokens=1500,
            )
        )
        
        full_text = ""
        async for chunk in response_stream:
            if chunk.text:
                full_text += chunk.text

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
