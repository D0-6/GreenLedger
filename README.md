# GreenLedger: Institutional Forensic Observatory

**Live Hackathon Debut | Llama 4 Maverick Edition**

GreenLedger is a premier forensic AI platform designed to audit corporate ESG claims against global telemetry nodes. It leverages the **NVIDIA Llama 4 Maverick** reasoning engine to synthesize institutional reports and provide verifiable credibility matrices.

## 🚀 Live Deployment Guide

The platform is architected for a high-performance hybrid deployment.

### 1. Backend & Forensic Engine (Railway)
The backend handles long-running Llama 4 audits and Playwright evidence capture.
- **Source**: `backend/`
- **Platform**: [Railway](https://railway.app/)
- **Environment Variables**:
  - `NVIDIA_API_KEY`: Your Llama 4 Maverick API key.
  - `DATABASE_URL`: Your Postgres connection string.
  - `PORT`: (Managed by Railway).

### 2. Frontend & Institutional UI (Vercel)
The Next.js 16.2 frontend delivers a premium global telemetry visualization.
- **Source**: `frontend/`
- **Platform**: [Vercel](https://vercel.com/)
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: Your deployed Railway Backend URL.

## 🛠 Features
- **Forensic PDF Upload**: Direct institutional document extraction via the `+` trigger.
- **Llama 4 Synergy**: Verification of claims against live G7 search indices.
- **9-Point Audit Report**: Automated export of high-fidelity PDF forensic reports.
- **Global Kinetic Sweep**: Real-time visualization of institutional nodes.

## ⚡ Quick Copy: Environment Variables

To make your deployment "Zero-Stress," copy these variables into your cloud dashboards.

### 1. Railway (Backend)
Add these in the **Variables** tab on Railway:
- `NVIDIA_API_KEY`: (Your NVIDIA API Key)
- `DATABASE_URL`: (Your Railway Postgres URL)

### 2. Vercel (Frontend)
Add this in **Settings > Environment Variables** on Vercel:
- `NEXT_PUBLIC_API_URL`: (Your Railway App URL, e.g., `https://greenledger-production.up.railway.app`)

---

## 🛠 Project Structure
- `📁 backend/`: FastAPI Forensic Engine (Llama 4 Maverick).
- `📁 frontend/`: Next.js Institutional UI.
- `📄 vercel.json`: Optimized Vercel routing.
- `📄 Procfile`: Railway process manager.

## 🛡 Security Note
Your `.env` file is ignored by Git to prevent your API keys from leaking to the public. Always use the Cloud Dashboards to manage secrets.

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
