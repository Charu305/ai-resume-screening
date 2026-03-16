# 📄 AI Resume Screening App — Gemini LLM + Multi-Agent

> **A production-deployed AI application** that automates resume screening against a job description using Google Gemini LLM — built with a multi-agent architecture, modular utility layer, Streamlit UI, and fully containerised with Docker for deployment.

---

## 📌 Project Overview

Recruiters spend hours manually screening hundreds of resumes for a single job opening. Most resumes are rejected in under 10 seconds based on keyword matching — missing strong candidates who used different terminology. This project replaces that process with an **intelligent AI screening system** that reads resumes the way a thoughtful recruiter would.

Given a job description and a set of resumes (PDF/text), the app uses **Google Gemini LLM** to:
- Understand the intent and requirements of the job description
- Evaluate each resume against those requirements with nuanced reasoning
- Score and rank candidates with structured justifications
- Highlight skill matches, gaps, and standout qualities per candidate

This is the most **production-complete** project in this portfolio — it goes beyond notebooks to a fully deployable application with a web UI, Docker container, and deployment documentation.

---

## 🎯 Problem Statement

> *Given a job description and multiple resumes, automatically screen, score, and rank candidates using an LLM — providing structured, explainable evaluations that a recruiter can act on immediately.*

**Why LLM-based screening beats keyword matching:**

| Keyword Matching (ATS) | LLM Screening (This App) |
|---|---|
| Rejects "ML Engineer" resume for "Machine Learning" role | Understands they are the same |
| Misses adjacent skills (e.g., PyTorch ≠ TensorFlow) | Recognises transferable skills |
| No context — treats every word equally | Understands seniority, impact, context |
| Cannot evaluate soft skills or project quality | Can reason about project descriptions |
| Binary pass/fail | Nuanced score with explanation |

---

## 🏗️ System Architecture

```
User Input (via Streamlit UI)
 ├── Job Description (text)
 └── Resume(s) (PDF upload)
            │
            ▼
┌─────────────────────────────────────┐
│          app.py (Streamlit UI)       │
│  Handles file upload, user input,   │
│  displays results and rankings      │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│       agents/  (Multi-Agent Layer)  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  JD Analyser Agent          │    │
│  │  Extracts key requirements, │    │
│  │  skills, and priorities     │    │
│  │  from the job description   │    │
│  └──────────────┬──────────────┘    │
│                 │                   │
│  ┌──────────────▼──────────────┐    │
│  │  Resume Evaluator Agent     │    │
│  │  Scores each resume against │    │
│  │  the extracted JD criteria  │    │
│  └──────────────┬──────────────┘    │
│                 │                   │
│  ┌──────────────▼──────────────┐    │
│  │  Ranking Agent              │    │
│  │  Compares all candidates    │    │
│  │  and produces final ranking │    │
│  │  with justifications        │    │
│  └─────────────────────────────┘    │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│       utils/  (Utility Layer)        │
│  PDF text extraction                │
│  Prompt templates                   │
│  Gemini API client                  │
│  Response parsing & formatting      │
└────────────────┬────────────────────┘
                 │
                 ▼
         Google Gemini LLM API
                 │
                 ▼
   Structured Candidate Evaluation
   Score + Match Analysis + Ranking
```

---

## 🗂️ Project Structure

```
ai-resume-screening/
│
├── app.py                          # Streamlit web application — UI entry point
├── agents/                         # Multi-agent logic layer
│   ├── jd_analyser.py              # Extracts structured requirements from JD
│   ├── resume_evaluator.py         # Scores each resume against JD criteria
│   └── ranking_agent.py            # Ranks all candidates and generates report
├── utils/                          # Reusable utility functions
│   ├── pdf_parser.py               # Extracts clean text from uploaded PDF resumes
│   ├── gemini_client.py            # Google Gemini API wrapper
│   └── prompt_templates.py         # All LLM prompt templates (centralised)
├── Dockerfile                      # Container definition for deployment
├── requirements.txt                # Python dependencies
└── AI_Resume_Deploy_Commands.pdf   # Step-by-step deployment guide
```

---

## 🔬 Technical Deep Dive

### 1. Multi-Agent Architecture (`agents/`)

The screening task is broken into three specialised agents — each with a single, well-defined responsibility:

**Agent 1 — JD Analyser**
- Receives the raw job description text
- Prompts Gemini to extract structured requirements:
  - Must-have skills (hard requirements)
  - Nice-to-have skills (preferred)
  - Experience level and seniority
  - Domain knowledge required
  - Soft skills and cultural signals
- Returns a structured JSON object used by downstream agents

**Agent 2 — Resume Evaluator**
- Receives a single resume + the structured JD analysis from Agent 1
- Prompts Gemini to evaluate the resume against each extracted criterion
- Returns a structured score (0–100) with per-criterion breakdown and reasoning
- Runs independently per resume — parallelisable for large batches

**Agent 3 — Ranking Agent**
- Receives all evaluated resumes with their scores
- Prompts Gemini to perform a holistic comparison — not just score sorting
- Generates a final ranked list with:
  - Overall recommendation (Strongly Recommend / Consider / Reject)
  - Top 3 strengths per candidate
  - Key gaps per candidate
  - Differentiators that distinguish top candidates

### 2. Utility Layer (`utils/`)

**`pdf_parser.py`** — Extracts clean, structured text from uploaded PDF resumes using `pdfplumber` / `PyPDF2`. Handles multi-column layouts, bullet points, and common resume formatting.

**`gemini_client.py`** — A clean wrapper around the Google Gemini API:
```python
# Single responsibility: send prompt, return response
def call_gemini(prompt: str, model: str = "gemini-pro") -> str:
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text
```
Centralising the API call means swapping Gemini for GPT-4 or Claude requires changing one file.

**`prompt_templates.py`** — All LLM prompts are stored as Python string templates in one place. This is the **most important engineering decision** in the project — separating prompt logic from agent logic means prompts can be iterated and improved without touching agent code.

### 3. Streamlit UI (`app.py`)

- **Job Description input** — text area for pasting the JD
- **Resume uploader** — multi-file PDF upload
- **Run Screening button** — triggers the full agent pipeline
- **Results panel** — displays ranked candidates with scores, match breakdown, and recommendations
- **Download report** — exports screening results as a structured report

### 4. Docker Containerisation (`Dockerfile`)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

Containerising the app means:
- **Reproducible environment** — works identically on any machine
- **Cloud deployment ready** — directly deployable to GCP Cloud Run, AWS ECS, or Azure Container Instances
- **No dependency conflicts** — isolated from the host system

---

## 📊 What the App Outputs

For each resume evaluated against the job description:

```
Candidate: [Name from resume]
Overall Score: 82 / 100
Recommendation: ✅ Strongly Recommend

Skill Match:
  ✅ Python (Required) — 5 years demonstrated experience
  ✅ Machine Learning (Required) — Multiple production projects
  ✅ SQL (Required) — Evidenced across 3 roles
  ⚠️  AWS (Preferred) — No direct mention, Azure experience present
  ❌ Kubernetes (Nice-to-have) — Not mentioned

Strengths:
  • Strong NLP and GenAI project history aligns closely with role
  • Led cross-functional teams — matches senior-level expectation
  • Published open-source contributions — signals technical initiative

Gaps:
  • No explicit cloud deployment experience at scale
  • Preferred fintech domain experience absent

Differentiator:
  • Only candidate with direct RAG implementation experience
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.11 |
| LLM | Google Gemini (`gemini-pro`) via `google-generativeai` |
| Web UI | Streamlit |
| PDF Parsing | pdfplumber / PyPDF2 |
| Containerisation | Docker |
| Deployment | GCP Cloud Run / AWS ECS / Any Docker host |
| Architecture | Multi-agent (custom, no framework dependency) |

---

## 🚀 How to Run

### Option A — Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Charu305/ai-resume-screening.git
cd ai-resume-screening

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Gemini API key
export GOOGLE_API_KEY="your-gemini-api-key"

# 4. Launch the app
streamlit run app.py
# Open http://localhost:8501
```

### Option B — Run with Docker

```bash
# 1. Build the container
docker build -t ai-resume-screening .

# 2. Run the container
docker run -p 8501:8501 -e GOOGLE_API_KEY="your-key" ai-resume-screening

# 3. Open http://localhost:8501
```

### Option C — Deploy to Cloud

See `AI_Resume_Deploy_Commands.pdf` for step-by-step instructions for:
- GCP Cloud Run deployment
- AWS ECS deployment
- Environment variable management in production

---

## 💡 Key Learnings & Takeaways

- **Prompt templates as first-class code** — storing all prompts in `prompt_templates.py` rather than embedding them in agent logic is the single most important maintainability decision. Prompts are the "weights" of an LLM application — they deserve the same version control discipline as code.
- **Multi-agent separation of concerns** — splitting JD analysis, resume evaluation, and ranking into three agents makes each independently testable and improvable. Changing the ranking logic doesn't risk breaking resume evaluation.
- **Gemini client abstraction** — wrapping the API in a single `call_gemini()` function means the entire app can switch LLM providers by changing one file. This is the right pattern for production AI applications.
- **Docker is non-negotiable for reproducibility** — packaging the app in a container means it runs identically in development, CI, and production. Every AI application that goes beyond a personal notebook should be containerised.
- **Structured LLM output requires structured prompting** — getting Gemini to reliably return JSON-formatted scores and breakdowns requires explicit output format instructions in the prompt. Free-form responses are unparseable at scale.
- **LLM screening is explainable by design** — unlike a black-box ML classifier, every screening decision comes with a written justification from the LLM. This is a critical advantage for any HR-adjacent AI application where auditability matters.

---

## 🔮 Potential Enhancements

- **Batch processing** — screen 50+ resumes in parallel using async Gemini calls
- **Bias detection layer** — an additional agent that flags potentially biased screening criteria in the JD
- **ATS integration** — connect to Workday, Greenhouse, or Lever APIs to pull JDs and push screening results directly
- **Interview question generation** — a fourth agent that generates role-specific interview questions based on each candidate's profile and identified gaps
- **Feedback loop** — capture recruiter overrides and use them to improve prompt quality over time

---

## 👩‍💻 Author

**Charunya**
🔗 [GitHub Profile](https://github.com/Charu305)

---

## 📄 License

This project is developed for educational and research purposes.
