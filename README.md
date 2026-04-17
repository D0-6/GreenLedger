# GreenLedger: ESG Forensic Verification System

An "Architectural Blueprint" platform for corporate ESG (Environmental, Social, Governance) forensic analysis. GreenLedger provides an immutable record of sustainability claims, verified by AI and live search data.

## Final Tech Stack (Locked)

- **Frontend**: Next.js 15 (App Router) + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI (Python)
- **Database**: Railway Postgres
- **AI**: OpenAI gpt-4o-mini (Zero Temperature)
- **Live Search**: DuckDuckGo (ddgs)
- **Report Generation**: python-docx (In-memory)

## Design System: The Architectural Blueprint

GreenLedger uses a high-precision, engineered design system:
- **Palette**: Slate, Navy, and Steel (#565e74 primary).
- **Strokes**: Rigorous 1px solid borders, no soft shadows.
- **Typography**: Precision Inter-only spec.
- **Density**: High information density for professional forensic workflows.

## Architecture

```mermaid
graph TD
    A[ESG Input] --> B[Forensic Engine]
    B --> C[DuckDuckGo Search]
    C --> D[OpenAI GPT-4o-mini]
    D --> E[Risk Scoring]
    E --> F[Public Ledger]
    F --> G[Word Report]
```

## Setup & Installation

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (Railway recommended)

### 2. Backend Setup
```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Configuration
Create a `.env` file in the root:
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=sk-...
```

## Features

- **Forensic Module**: Real-time analysis with execution logs.
- **Ledger Explorer**: Irreversible record of claims with SHA-256 identification.
- **Risk Scoring**: 0-100 analysis with Greenwashing red flags detection.
- **Word Reports**: Professional documentation generation.

---
**Status**: Production Ready (Architectural Redesign Complete)
