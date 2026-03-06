# Philo-RAG (철학자와의 대화)
> ⚠️ **안내사항 (Cold Start)**
> 본 프로젝트의 백엔드 서버는 무료 클라우드 인스턴스에 배포되어 운영 중입니다. 일정 시간 요청이 없으면 서버가 휴면 상태로 전환되므로, **최초 접속 시 (Cold start) 백엔드 응답까지 약 1분 정도의 대기 시간이 발생**할 수 있습니다. 

**실제 배포된 사이트 URL:** https://philo-rag.vercel.app/

**Philo-RAG**는 위대한 철학자들의 저술과 사상을 바탕으로, 사용자의 질문에 답변을 제공하는 대화형 RAG(Retrieval-Augmented Generation) 웹 애플리케이션입니다.

---

## 🏗 아키텍처 및 기술 스택 (Architecture & Tech Stack)

본 애플리케이션은 **Next.js (App Router)** 기반의 프론트엔드와 **FastAPI** 기반의 백엔드로 완전히 분리되어 작동하는 현대적인 마이크로서비스 지향 구조를 가집니다.

### 프론트엔드 (Frontend)
- **Framework**: Next.js 16.1.6 (React 19.2.4)
- **Styling**: Tailwind CSS, Lucide React (Icons)
- **Language**: TypeScript
- **State Management**: React Hooks (`useState`, `useRef`, `useCallback`)
- **Key Features**: 
  - `fetch` API의 `ReadableStream`을 활용한 커스텀 SSE 스트리밍 UI 구현
  - `IntersectionObserver`를 활용한 가시성 기반 메타데이터 동적 로딩 (스크롤 위치에 따른 컨텍스트 소스 변경)
  - 다크모드 기반의 미려하고 반응형(Responsive)을 지원하는 컴포넌트 설계

### 백엔드 (Backend)
- **Framework**: FastAPI (Python 3.10+)
- **LLM/AI Model**: Google Gemini API (`gemini-2.5-flash`)
- **RAG & Vector Store**: LangChain, Supabase pgvector
- **Embeddings**: HuggingFace (`jhgan/ko-sroberta-multitask`)
- **Key Features**:
  - `SSE-Starlette`를 적용한 비동기 스트리밍 응답 (응답 지연 감소)
  - LangChain 기반의 문서 청킹(Chunking) 및 벡터DB 구축
  - 철학자 이름 및 서적 메타데이터를 클라이언트에 실시간 이벤트로 전송하여 사용자 경험 강화
  - Rate-limit 대응 및 에러 핸들링 (에러 발생 시 스트리밍 중단 및 클라이언트에 명확한 에러 메시지 전달)

---

## 🔄 데이터 흐름 (Data Flow)

Philo-RAG의 주요 질문-답변 파이프라인은 다음과 같이 작동합니다.

1. **Question Input**: 사용자가 프론트엔드 UI를 통해 질문을 입력합니다.
2. **Streaming Request**: 프론트엔드는 이전 대화 기록(Context)과 함께 백엔드 FastAPI 엔드포인트에 `POST` 요청을 보냅니다.
3. **Vector Search (Retrieval)**: FastAPI는 사용자의 질문을 임베딩 모델을 통해 벡터화하고, Supabase(pgvector)에서 가장 유사도가 높은 철학 서적 청크(문서 조각)를 검색합니다.
4. **Metadata Extraction**: 검색된 문서를 바탕으로 어떤 철학자와 어떤 책에서 인용되었는지 메타데이터를 추출합니다.
5. **LLM Generation**: 검색된 문서 내용(Context)과 대화 기록, 사용자 질문을 조합하여 Gemini 모델에게 프롬프트로 전달합니다.
6. **SSE Streaming**: 
   - 모델 응답 전 1단계: 먼저 추출된 메타데이터를 JSON 형태로 직렬화하여 클라이언트에 스트리밍 `event: metadata`로 전송합니다.
   - 모델 응답 전 2단계: 이어서 LLM이 생성해내는 답변을 청크 단위로 클라이언트에 스트리밍 `event: content`로 전송합니다.
7. **Client Rendering**: 프론트엔드는 이벤트를 수신하여 메타데이터 기반으로 참고문헌(Citation) 카드를 생성하고, 답변 텍스트를 타이핑 애니메이션처럼 실시간으로 렌더링합니다.

---

## 🌟 주요 특징 (Key Features)

- **출처 표기 기능 (Citation Cards)**: AI가 답변을 생성할 때 참고한 철학자 이름과 책 제목의 메타데이터를 보여주어 환각(Hallucination)을 방지하고 신뢰도를 높입니다.
- **스크롤 반응형 컨텍스트 메뉴**: 대화 내용이 길어질 경우, 사용자가 스크롤을 올려 과거의 AI 응답을 보고 있으면 좌측 사이드바가 해당 응답 당시의 철학자 메타데이터로 즉시 업데이트됩니다 (`IntersectionObserver` 활용).
- **스트리밍 기반의 빠른 체감 속도**: RAG의 고질적인 문제인 '시간 지연'을 최소화하기 위해 답변을 청크별로 즉시 화면에 띄웁니다.

---

## 💡 사용 예시 (Usage Examples)

1. **행복에 대한 질문**: "진정한 행복이란 무엇이라고 생각하시나요?"
   - 결과: AI는 데이터베이스 내의 다양한 철학 서적을 검색하여, '행복'에 대한 여러 철학자들의 통찰력을 바탕으로 실시간 답변을 작성합니다.
2. **윤리적 딜레마 질문**: "인간 관계에서 거짓말은 어떠한 경우에도 정당화될 수 없나요?"
   - 결과: 우측 화면에 도덕·윤리 관련 출처 카드(알라딘 도서 표지 및 메타데이터 사전 로드)가 표시되며, 여러 관점을 혼합한 구조적 답변이 스트리밍됩니다.
3. **사회적 질문**: "이상적이고 평등한 국가란 어떤 모습이어야 할까요?"
   - 결과: 정치/사회 철학과 관련된 도서 메타데이터를 RAG 파이프라인으로 찾아 직설적이고 다각적인 답변을 제시합니다.

---

## 💻 실행 방법 (Local Setup)

### 사전 요구 사항
- Node.js
- Python 3.10+
- Supabase 프로젝트 & Gemini API 키

### 백엔드 설정 (Backend)
```bash
cd backend
python -m venv .venv
# 가상환경 활성화 (.venv\Scripts\activate - Windows 환경)
pip install -r requirements.txt

# .env.example을 참고하여 .env 파일 생성
echo "GEMINI_API_KEY=your_key" > .env
echo "SUPABASE_URL=your_url" >> .env
echo "SUPABASE_SERVICE_KEY=your_service_key" >> .env

# FastAPI 서버 실행
uvicorn app.main:app --reload
```

### 프론트엔드 설정 (Frontend)
```bash
cd frontend
npm install

# .env.local 파일 생성
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local

# Next.js 클라이언트 실행
npm run dev
```
이후 `http://localhost:3000`에 접속하여 서비스를 이용하실 수 있습니다.

---
---

# Philo-RAG (Philosophical Discourse)

**Philo-RAG** is an interactive RAG (Retrieval-Augmented Generation) web application that provides profound answers based on the writings and thoughts of great philosophers.

---

## 🏗 Architecture & Tech Stack

The application employs a modern microservices-oriented architecture, completely decoupling the **Next.js (App Router)** frontend from the **FastAPI** backend.

### Frontend
- **Framework**: Next.js 16.1.6 (React 19.2.4)
- **Styling**: Tailwind CSS, Lucide React (Icons)
- **Language**: TypeScript
- **State Management**: Enhanced React Hooks (`useState`, `useRef`, `useCallback`)
- **Key Features**: 
  - Custom SSE streaming UI utilizing the `ReadableStream` of the native `fetch` API.
  - Visibility-based dynamic metadata loading using `IntersectionObserver` (changing context sources based on user scroll position).
  - A sleek, responsive, dark-mode native component design system.

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **LLM/AI Model**: Google Gemini API (`gemini-2.5-flash`)
- **RAG & Vector Store**: LangChain, Supabase pgvector
- **Embeddings**: HuggingFace (`jhgan/ko-sroberta-multitask`)
- **Key Features**:
  - Asynchronous streaming responses using `SSE-Starlette` to minimize perceived latency.
  - Vector database construction and document chunking using LangChain.
  - Real-time transmission of metadata (philosopher names, book titles) as specific server events to enhance UX.
  - Handling of external API rate limits and robust fail-safes (terminating the stream cleanly if errors occur).

---

## 🔄 Data Flow Pipeline

The core Q&A pipeline operates as follows:

1. **Question Input**: The user inputs a query through the UI.
2. **Streaming Request**: The frontend sends a `POST` request to the FastAPI endpoint, attaching the conversation history as context.
3. **Vector Search (Retrieval)**: FastAPI categorizes the query, converts it into an embedding vector, and searches Supabase (pgvector) for the most semantically similar philosophical text chunks.
4. **Metadata Extraction**: Metadata (Author, Title) from the retrieved documents is pooled and analyzed.
5. **LLM Generation**: The retrieved context, conversation history, and user query are combined into a prompt and sent to the Gemini model.
6. **SSE Streaming Starts**: 
   - Output 1: The extracted metadata is serialized as JSON and streamed to the client via an `event: metadata` signal.
   - Output 2: The LLM's generated response is streamed chunk-by-chunk via `event: content`.
7. **Client Rendering**: The frontend listens to these distinct events. It renders the metadata as a citation/source card instantly and updates the AI response text with a typing effect as chunks arrive.

---

## 🌟 Key Features

- **Dynamic Citation Cards**: Displaying the philosopher's name and book origin helps prevent AI hallucinations and builds high reliability.
- **Scroll-Responsive Context Sidebar**: If the conversation grows long and the user scrolls up to an older AI response, the left sidebar automatically reads the metadata for that exact message and updates the sources visually (`IntersectionObserver`).
- **High-Speed Streaming UX**: Addressing the common latency issue of RAG pipelines by actively streaming tokens the moment the LLM begins generation.

## 💡 Usage Examples

1. **Question about Happiness**: "What do you think true happiness is?"
   - Result: AI searches various philosophical books in the database and streams a real-time answer based on insights from multiple philosophers regarding 'happiness'.
2. **Ethical Dilemma Question**: "Can lying in human relationships ever be justified?"
   - Result: Source cards related to morality or ethics (with book covers and metadata pre-loaded) appear on the right pane, while a structured answer combining different perspectives is streamed.
3. **Social Question**: "What should an ideal and egalitarian state look like?"
   - Result: Uses the RAG pipeline to locate metadata on political/social philosophy books and provides a direct, multifaceted answer.

---

## 💻 How to Run (Local Setup)

> ⚠️ **Notice (Cold Start)**
> The backend server is currently hosted on a free cloud instance. If there are no requests for a while, the server enters a sleep state. Therefore, **upon your first access (cold start), it may take approximately 1 minute for the backend to respond**.

### Prerequisites
- Node.js
- Python 3.10+
- A Supabase Instance & Gemini API Key

### Backend Setup
```bash
cd backend
python -m venv .venv
# Activate venv (.venv\Scripts\activate on Windows)
pip install -r requirements.txt

# Create .env file based on .env.example
echo "GEMINI_API_KEY=your_key" > .env
echo "SUPABASE_URL=your_url" >> .env
echo "SUPABASE_SERVICE_KEY=your_service_key" >> .env

# Run FastAPI Server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local

# Run Next.js Server
npm run dev
```
Open `http://localhost:3000` to start using the system.
