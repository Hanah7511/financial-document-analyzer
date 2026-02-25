# AI Financial Document Analyzer – Debugged CrewAI System

## 📌 Overview
This project is a fixed and enhanced version of the provided CrewAI-based Financial Document Analyzer.  
The original repository contained multiple deterministic bugs, inefficient prompts, and non-functional tool integrations that prevented the system from working correctly.

The goal of this assignment was to debug the existing codebase (not rebuild it) and ensure:
- Functional document analysis pipeline
- Correct tool execution
- Efficient and grounded prompts
- Proper multi-agent workflow

The core architecture (CrewAI + FastAPI + Agents + Tasks) has been preserved while fixing critical issues.


This submission specifically addresses both categories mentioned in the assignment:
- Deterministic runtime bugs (tool crashes, file pipeline issues)
- Inefficient prompts causing hallucinated and unreliable outputs

---

# 🐛 Bugs Identified and Fixes Applied

## 1. Broken LLM Initialization (agents.py)
### Issue:
- Undefined or poorly configured LLM
- Risk of hallucinations and inconsistent outputs

### Fix:
- Implemented proper Google Gemini LLM configuration
- Reduced temperature to 0.2 for deterministic financial analysis
- Added environment-based API key loading

---

## 2. Inefficient and Malicious Prompts (task.py) ⭐ (Major Requirement)
### Issue:
Original tasks encouraged:
- Hallucinated financial advice
- Fake URLs
- Ignoring user queries
- Contradictory outputs

This violated real-world AI reliability standards.

### Fix:
- Rewrote task prompts to be structured and grounded
- Added clear analytical steps (Verification → Analysis → Risk → Investment)
- Ensured responses are based only on document content
- Implemented context chaining between tasks for logical reasoning

---

## 3. Non-Functional PDF Tool (tools.py) – Deterministic Runtime Bug
### Issue:
- Used undefined `Pdf()` loader (caused immediate crash)
- No error handling
- Improper async structure

### Fix:
- Replaced with `PyPDFLoader` from langchain_community
- Added file existence validation
- Implemented exception handling
- Converted tool to `@staticmethod` for proper CrewAI integration
- Cleaned extracted text for better LLM processing

---

## 4. Uploaded File Was Not Being Analyzed (main.py) – Critical Logic Bug
### Issue:
The original pipeline did not pass the uploaded file path to the Crew.
As a result, the system ignored user-uploaded financial documents and produced irrelevant analysis.

### Fix:
- Modified Crew kickoff inputs to include `file_path`
- Ensured dynamic file handling for uploaded PDFs
- Implemented proper file storage and cleanup using BackgroundTasks

---

## 5. Incomplete Multi-Agent Workflow
### Issue:
- Some agents lacked access to document tools
- Tasks were not logically sequenced

### Fix:
- Enabled tool access for all relevant agents
- Implemented sequential task execution:
  1. Document Verification
  2. Financial Analysis
  3. Risk Assessment
  4. Investment Recommendations

---

# 🧱 System Architecture (Preserved)
- FastAPI backend
- CrewAI multi-agent system
- Modular tools and tasks
- Sequential reasoning workflow
- PDF document ingestion pipeline

No framework changes were made to maintain the integrity of the original codebase.

---

# ⚙️ Setup Instructions

## 1. Clone Repository
```bash
git clone https://github.com/Hana7511/financial-document-analyzer.git
cd financial-document-analyzer
```

## 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4.  Set Environment Variables
Create a .env file in the root directory:
GOOGLE_API_KEY=your_google_gemini_api_key

## 5. Running the Application
uvicorn main:app --reload
Server will start at:
http://127.0.0.1:8000

📡 API Documentation
## 1. Analyze Financial Document
Endpoint:
POST /analyze

Request:

- file: PDF file (multipart/form-data)
- query: Optional analysis focus (form data)
- store_result: Boolean to store result (default: true)

Response:
{
  "status": "success",
  "analysis_id": "uuid",
  "timestamp": "2025-02-26T...",
  "query": "your query",
  "file_name": "document.pdf",
  "analysis": "comprehensive analysis text",
  "agents_used": ["verifier", "financial_analyst", "risk_assessor", "investment_advisor"]
}

## 2. Get Previous Analysis
GET /result/{analysis_id}

## 3. Health Check
GET /health


## 📊 Key Improvements Over Original Codebase

- Fixed deterministic runtime crashes
- Eliminated hallucination-prone prompts
- Enabled correct PDF-based analysis
- Implemented structured multi-agent reasoning
- Improved reliability and maintainability
- Preserved original architecture while stabilizing functionality

## 🧠 Design Approach

This project focuses on debugging and stabilizing the provided codebase rather than rebuilding it.
All fixes were applied while maintaining the original CrewAI architecture, ensuring alignment with the assignment requirement to debug deterministic bugs and optimize inefficient prompts.


## 🔮 Future Enhancements (Bonus Scope)

- Redis/Celery queue worker for concurrent requests
- Database integration (PostgreSQL/SQLite) for persistent analysis storage
- Advanced financial metric extraction module
- RAG-based financial document grounding


