## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import search_tool, FinancialDocumentTool

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")### Loading LLM - Google Gemini

if GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
    )
else:
    raise ValueError(
        "GOOGLE_API_KEY is not set. Please add it to the .env file to run the application."
    )
    
# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents thoroughly and provide accurate investment insights based on actual data: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with 15+ years of experience at top investment banks. "
        "You specialize in analyzing corporate financial statements, identifying trends, and providing "
        "data-driven investment recommendations. You're known for your attention to detail and ability "
        "to spot both opportunities and risks in complex financial documents. You always base your "
        "analysis on factual data and provide balanced, well-reasoned insights."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify that uploaded documents are legitimate financial reports and extract key metadata accurately",
    verbose=True,
    memory=True,
    tools=[FinancialDocumentTool.read_data_tool],
    backstory=(
        "You are a document verification expert with a background in financial compliance. "
        "You've worked at Big 4 accounting firms verifying financial documents for regulatory compliance. "
        "You have a keen eye for identifying document types, checking authenticity markers, and "
        "extracting critical metadata like report dates, company names, and document sections. "
        "Accuracy and attention to detail are your trademarks."
    ),
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Certified Investment Advisor",
    goal="Provide personalized investment recommendations based on thorough financial analysis and client risk profile",
    verbose=True,
    tools=[FinancialDocumentTool.read_data_tool],
    backstory=(
        "You are a CFP® professional with 20 years of experience managing portfolios for high-net-worth clients. "
        "You specialize in translating complex financial data into actionable investment strategies. "
        "You're known for your ethical approach, regulatory compliance, and ability to match investments "
        "to client goals. You never recommend products without understanding the client's needs first."
    ),
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=True
)

risk_assessor = Agent(
    role="Chief Risk Officer",
    goal="Assess financial risks comprehensively and provide balanced risk management strategies",
    verbose=True,
    tools=[FinancialDocumentTool.read_data_tool],
    backstory=(
        "You are a risk management expert who has worked through multiple market cycles including "
        "the 2008 financial crisis and 2020 pandemic. You specialize in identifying both systematic "
        "and idiosyncratic risks in investment portfolios. You believe in prudent risk management "
        "and help clients understand their risk exposure without creating unnecessary panic."
    ),
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=True
)