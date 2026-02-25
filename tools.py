## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path
        
        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.
            
        Returns:
            str: Full Financial Document content as text
        """
        try:
            if not os.path.exists(path):
                return f"Error: File not found at {path}"
            
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            full_report = ""
            for doc in docs:
                content = doc.page_content
                # Clean up the text
                content = ' '.join(content.split())  # Remove extra whitespace
                full_report += content + "\n\n"
            
            return full_report if full_report else "No text content extracted from PDF"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool:
    def analyze_investment_tool(self, financial_document_data):
        """Analyze financial data for investment insights"""
        # Process and analyze the financial document data
        if not financial_document_data:
            return "No financial data provided for analysis"
        
        # Basic analysis logic - in production, this would be more sophisticated
        analysis = {
            "document_length": len(financial_document_data),
            "has_financial_terms": any(term in financial_document_data.lower() 
                                      for term in ['revenue', 'profit', 'loss', 'earnings', 'cash']),
            "preview": financial_document_data[:500] + "..." if len(financial_document_data) > 500 else financial_document_data
        }
        
        return f"Investment analysis complete. Document size: {analysis['document_length']} characters. Contains financial terms: {analysis['has_financial_terms']}"

## Creating Risk Assessment Tool
class RiskTool:
    def create_risk_assessment_tool(self, financial_document_data):
        """Create risk assessment from financial data"""
        if not financial_document_data:
            return "No financial data provided for risk assessment"
        
        # Basic risk assessment - would be more sophisticated in production
        risk_indicators = []
        if 'debt' in financial_document_data.lower():
            risk_indicators.append("Debt mentioned - requires further analysis")
        if 'volatility' in financial_document_data.lower():
            risk_indicators.append("Volatility indicators present")
        
        return f"Risk assessment complete. Identified {len(risk_indicators)} risk factors: {', '.join(risk_indicators) if risk_indicators else 'No immediate risk factors identified'}"