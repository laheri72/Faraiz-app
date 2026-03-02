# Fatemi Wirasat Engine

A deterministic inheritance reasoning engine based strictly on the jurisprudence of *Daim al-Islam Bab al-Faraiz*.

## System Architecture

This application operates fundamentally differently from a standard inheritance calculator. It is a **deterministic rule engine** executing in layers:
1. **Layer 4 (Special Cases):** Edge cases like Grandchildren substitution (`ولد الولد يقوم مقام الولد`).
2. **Layer 1 (Children):** Direct descendant resolution.
3. **Layer 2 (Fixed Shares):** Quranic allocations (1/2, 1/3, 1/4, 1/6, 1/8, 2/3).
4. **Layer 3 (Priority Engine):** Kinship priority blocking (`الأقرب يمنع الأبعد`) and remainder distribution (`الرد بالرحم`).
5. **Layer 5 (Math Engine):** Exact symbolic fractional unification and calculation.

## Project Structure

```text
faraiz-app/
├── backend/                # Python FastAPI + SQLAlchemy + Rule Engine
│   ├── app/
│   │   ├── api/            # REST API Routes
│   │   ├── core/           # Configuration & App Settings
│   │   ├── database/       # DB Connection & Schema
│   │   └── engine/         # The Jurisprudence Logic Core
│   └── tests/              # Verification & Validation Scripts
├── frontend/               # React + Vite + TypeScript
│   ├── src/
│   │   ├── api/            # Axios API Clients
│   │   ├── pages/          # Primary UI Views
│   │   ├── types/          # Shared Interfaces
│   │   └── styles/         # CSS Styling
└── docker-compose.yml      # Orchestrates Postgres, Backend, and Frontend
```

## Quick Start

### 1. Installation
Install all dependencies for both Frontend and Backend from the root:
```bash
npm run install:all
```

### 2. Development
Run both Frontend (Vite) and Backend (FastAPI) concurrently from the root:
```bash
npm run dev
```
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000/api
- **API Docs:** http://localhost:8000/docs

### 3. Docker (Production Ready)
Ensure Docker Desktop is running, then execute:
```bash
docker-compose up --build
```

## Testing & Validation
The engine logic has been heavily validated against core principles. To run the verification scripts:
```bash
npm run test  # Runs backend/tests/comprehensive_test.py
```
