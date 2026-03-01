# PhiloRAG

PhiloRAG is a conversational RAG interface focusing on philosophical discussions. The project consists of a Next.js frontend and a FastAPI (Python) backend using LangChain and Google's Gemini models.

## Getting Started

### Prerequisites
- Node.js (for frontend)
- Python 3.10+ (for backend)

### 1. Backend Setup (FastAPI)

Navigate to the `backend` directory from the root of the project:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables:
Create a `.env` file in the `backend` directory based on the `.env.example` structure.
You will need your `GEMINI_API_KEY`, as well as `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` which are required by the backend configuration (`app/core/config.py`).
```bash
# example .env contents
GEMINI_API_KEY="your-api-key-here"
SUPABASE_URL="your-supabase-url"
SUPABASE_SERVICE_KEY="your-supabase-service-key"
```

Start the backend server on `http://localhost:8000`:
```bash
uvicorn app.main:app --reload
```
You can access the generated API docs at `http://localhost:8000/docs`.

---

### 2. Frontend Setup (Next.js)

Navigate to the `frontend` directory from the root of the project:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Set up environment variables:
Create a `.env.local` file (or `.env` depending on your setup) and specify the backend API base url if needed:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Start the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Architecture Highlights
- Frontend: Next.js 14+ (App Router), TailwindCSS, TypeScript, custom SSE streaming integration.
- Backend: FastAPI, LangChain, HuggingFace embedding, and Supabase integration.
