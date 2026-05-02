# GreenLedger: Vercel/Gemini Edition

## Project Overview
GreenLedger is an institutional-grade ESG (Environmental, Social, and Governance) verification platform designed to detect greenwashing. It analyzes corporate sustainability claims against global regulatory standards and live telemetry, providing a definitive risk score and storing the proof on an immutable ledger.

## Core Directives
1. **Unbreakable Reliability**: The platform must gracefully handle external API interruptions via forensic fallbacks, ensuring live hackathon demos never crash.
2. **Institutional Authority**: The UI and AI outputs must mimic high-end corporate audit reports (e.g., "Step 3: Archive to Public Ledger").
3. **Vercel Native**: The entire stack (Next.js Frontend + Python FastAPI Backend) must be deployable to Vercel via Serverless Functions.
4. **Gemini Engine**: The AI core relies strictly on `gemini-2.5-flash` for high-speed, parallel reasoning.

## Technology Stack
- **Frontend**: Next.js (React), TailwindCSS
- **Backend**: Python 3.12, FastAPI (deployed to Vercel `/api`)
- **AI Model**: Google Gemini (`google-genai` SDK)
- **Live Search**: DuckDuckGo Telemetry Engine (`ddgs`)
- **Database**: PostgreSQL (Railway)

## High-Level Architecture
1. User enters claim in the Next.js UI.
2. Frontend triggers `/api/analyze` (Serverless Function).
3. FastAPI backend executes a parallel telemetry sweep.
4. Gemini 2.5 Flash synthesizes the data into a 9-Point Audit Structure.
5. User clicks "Archive to Public Ledger" triggering `/api/save-to-ledger`.
6. Record is hashed and committed to Railway Postgres.
