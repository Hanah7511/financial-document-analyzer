## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import FinancialDocumentTool

## Verification Task - First in sequence
verification_task = Task(
    description="""Verify if the uploaded document is a legitimate financial report.
    
    Steps:
    1. Read the document content from the provided path
    2. Identify document type, company name, report period if available
    3. Check for key financial sections (balance sheet, income statement, cash flow)
    4. Provide verification status and document metadata
    
    User query: {query}
    Document path: {file_path}
    """,
    
    expected_output="""A structured verification report containing:
    - Document type verification (is it a financial document? yes/no)
    - Company name (if identifiable)
    - Report period/date
    - Key sections identified
    - Confidence score (0-100%)
    - Any red flags or concerns
    """,
    
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Financial Analysis Task - Second
analysis_task = Task(
    name="Financial Analysis",
    description="""Analyze the financial document thoroughly.
    
    Based on the verified document, provide comprehensive financial analysis:
    1. Extract key financial metrics (revenue, profit, margins, etc.)
    2. Identify trends and significant changes
    3. Compare with industry benchmarks if available
    4. Highlight notable achievements or concerns
    5. Answer the user's specific query: {query}
    
    Use the verified document content from the verification step.
    """,
    
    expected_output="""A detailed financial analysis including:
    - Executive summary of financial health
    - Key metrics table with period-over-period changes
    - Trend analysis (at least 3 key trends)
    - Strengths identified (3-5 points)
    - Areas of concern (3-5 points)
    - Direct answer to user's query
    """,
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    context=[verification_task],  # Depends on verification
    async_execution=False,
)

## Risk Assessment Task - Third
risk_assessment_task = Task(
    name="Risk Assessment",
    description="""Evaluate risks based on the financial analysis.
    
    Using the financial analysis results, provide comprehensive risk assessment:
    1. Identify financial risks (liquidity, solvency, profitability risks)
    2. Assess market and operational risks
    3. Evaluate regulatory and compliance risks
    4. Provide risk ratings (low/medium/high) with justification
    5. Suggest risk mitigation strategies
    
    User query context: {query}
    """,
    
    expected_output="""A structured risk assessment with:
    - Overall risk rating (Low/Medium/High)
    - Categorized risks (Financial, Operational, Market, Regulatory)
    - Each risk with: description, likelihood, impact, mitigation strategy
    - Risk heat map or prioritization
    - Recommendations for risk management
    """,
    
    agent=risk_assessor,
    context=[analysis_task],  # Depends on analysis
    async_execution=False,
)

## Investment Recommendations Task - Fourth
investment_task = Task(
    name="Investment Recommendations",
    description="""Generate investment recommendations based on all previous analyses.
    
    Using the financial analysis and risk assessment, provide:
    1. Investment thesis for the company
    2. Specific recommendations (Buy/Hold/Sell) with rationale
    3. Suggested allocation based on risk profile
    4. Time horizon considerations
    5. Alternative investment options
    
    Address the user's specific query: {query}
    """,
    
    expected_output="""A comprehensive investment recommendation including:
    - Investment summary (1 paragraph)
    - Recommendation rating (Strong Buy/Buy/Hold/Sell/Strong Sell)
    - Key investment highlights (3-5 points)
    - Key risks to monitor (3-5 points)
    - Suggested position sizing (% of portfolio)
    - Price targets (if applicable)
    - Monitoring checklist
    """,
    
    agent=investment_advisor,
    context=[analysis_task, risk_assessment_task],  # Depends on both
    async_execution=False,
)