from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid
import shutil
from typing import Optional
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import verification_task, analysis_task, risk_assessment_task, investment_task

app = FastAPI(
    title="Financial Document Analyzer API",
    description="AI-powered financial document analysis with multi-agent crew",
    version="2.0.0"
)

# In-memory storage for demo - in production use database
analysis_results = {}

def run_financial_crew(query: str, file_path: str) -> dict:
    """Run the complete financial analysis crew with all agents"""
    
    # Create crew with all agents and tasks in sequence
    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
        tasks=[verification_task, analysis_task, risk_assessment_task, investment_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the crew with inputs
    result = financial_crew.kickoff(inputs={
        'query': query,
        'file_path': file_path
    })
    
    return result

@app.get("/")
async def root():
    """API health check endpoint"""
    return {
        "status": "online",
        "service": "Financial Document Analyzer",
        "version": "2.0.0",
        "endpoints": {
            "POST /analyze": "Upload and analyze financial document",
            "GET /result/{analysis_id}": "Retrieve previous analysis result"
        }
    }

@app.post("/analyze")
async def analyze_financial_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Financial document (PDF format)"),
    query: str = Form(default="Analyze this financial document and provide investment insights"),
    store_result: bool = Form(default=True, description="Store analysis result for later retrieval")
):
    """
    Upload a financial document and get comprehensive AI-powered analysis
    
    - **file**: PDF file containing financial report (required)
    - **query**: Specific question or analysis focus (optional)
    - **store_result**: Whether to store result for later retrieval (optional)
    
    Returns comprehensive analysis from all four specialized agents
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique IDs
    analysis_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{analysis_id}_{file.filename}"
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the financial document with all analysts
        result = run_financial_crew(query=query.strip(), file_path=file_path)
        
        response_data = {
            "status": "success",
            "analysis_id": analysis_id,
            "timestamp": timestamp,
            "query": query,
            "file_name": file.filename,
            "analysis": str(result),
            "agents_used": ["verifier", "financial_analyst", "risk_assessor", "investment_advisor"]
        }
        
        # Store result if requested
        if store_result:
            analysis_results[analysis_id] = response_data
            # Clean up old results in background (keep last 100)
            if len(analysis_results) > 100:
                oldest = min(analysis_results.keys())
                del analysis_results[oldest]
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        # Clean up file in background to not block response
        background_tasks.add_task(cleanup_file, file_path)

@app.get("/result/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """Retrieve a previously stored analysis result by ID"""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    return analysis_results[analysis_id]

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "storage": f"{len(analysis_results)} results cached",
        "agents": ["verifier", "financial_analyst", "risk_assessor", "investment_advisor"]
    }

def cleanup_file(file_path: str):
    """Background task to clean up temporary files"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)