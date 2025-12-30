import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import re
from app.config import Config


class GeminiService:
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        api_key = api_key or Config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        model_name = model_name or Config.GEMINI_MODEL
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def _build_schema_context(self, schema_info: Dict[str, Dict[str, Any]]) -> str:
        """Build a context string from schema information"""
        context_parts = []
        
        for sheet_name, info in schema_info.items():
            context_parts.append(f"\nSheet: {sheet_name}")
            context_parts.append(f"Columns: {', '.join(info['columns'])}")
            context_parts.append(f"Row count: {info['row_count']}")
            
            if info.get('sample_rows'):
                context_parts.append("Sample data (first few rows):")
                for i, row in enumerate(info['sample_rows'][:3], 1):
                    context_parts.append(f"  Row {i}: {row}")
        
        return "\n".join(context_parts)
    
    def _extract_code(self, text: str) -> str:
        """Extract Python code from Gemini response"""
        # Look for code blocks
        code_block_pattern = r'```(?:python)?\s*(.*?)```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, look for lines that look like code
        lines = text.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if any(keyword in line for keyword in ['import ', 'df.', 'pd.', '=']):
                in_code = True
            if in_code:
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        return text.strip()
    
    def generate_query_code(
        self, 
        question: str, 
        schema_info: Dict[str, Dict[str, Any]],
        dataframes_var_name: str = "dataframes"
    ) -> str:
        """Generate pandas code to answer a question"""
        schema_context = self._build_schema_context(schema_info)
        
        # Build sheet list for context
        sheet_names = list(schema_info.keys())
        sheets_context = f"Available sheets: {', '.join(sheet_names)}" if len(sheet_names) > 1 else f"Sheet: {sheet_names[0]}"
        
        prompt = f"""You are a data analyst assistant. You have access to financial data stored in a dictionary called '{dataframes_var_name}' where keys are sheet names and values are pandas DataFrames.

{sheets_context}

Data structure:
{schema_context}

User question: {question}

Generate Python pandas code to answer this question. The code should:
1. Access dataframes from the '{dataframes_var_name}' dictionary using sheet names as keys (e.g., dataframes['Sheet1'])
2. If the question doesn't specify a sheet, intelligently select the most relevant sheet(s) based on column names and data
3. If multiple sheets are needed, you can merge/join them or process them separately
4. Perform necessary operations (filtering, grouping, aggregations, etc.)
5. Store the final result in a variable called 'result'
6. Handle cases where data might be in different sheets - check column names to find the right sheet

Important:
- Always use dataframes['SheetName'] to access a specific sheet
- If unsure which sheet, check column names across sheets
- You can iterate over sheets if needed: for sheet_name, df in dataframes.items()
- Handle missing data gracefully

Return ONLY the Python code, no explanations or markdown formatting. The code should be executable as-is.
"""
        
        try:
            response = self.model.generate_content(prompt)
            code = self._extract_code(response.text)
            return code
        except Exception as e:
            raise Exception(f"Error generating code with Gemini: {str(e)}")
    
    def generate_chart_code(
        self,
        request: str,
        schema_info: Dict[str, Dict[str, Any]],
        dataframes_var_name: str = "dataframes"
    ) -> str:
        """Generate code to create a visualization"""
        schema_context = self._build_schema_context(schema_info)
        
        # Build sheet list for context
        sheet_names = list(schema_info.keys())
        sheets_context = f"Available sheets: {', '.join(sheet_names)}" if len(sheet_names) > 1 else f"Sheet: {sheet_names[0]}"
        
        prompt = f"""You are a data visualization assistant. You have access to financial data stored in a dictionary called '{dataframes_var_name}' where keys are sheet names and values are pandas DataFrames.

{sheets_context}

Data structure:
{schema_context}

User request: {request}

Generate Python code using plotly to create the requested visualization. The code should:
1. Access dataframes from the '{dataframes_var_name}' dictionary using sheet names as keys (e.g., dataframes['Sheet1'])
2. If the request doesn't specify a sheet, intelligently select the most relevant sheet based on column names
3. If multiple sheets are needed, you can merge/join them or create subplots
4. Prepare the data for visualization
5. Create a plotly figure (use plotly.graph_objects or plotly.express)
6. Store the figure in a variable called 'fig'
7. Convert the figure to JSON using: chart_json = fig.to_json()

Important:
- Always use dataframes['SheetName'] to access a specific sheet
- Check column names across sheets to find the right data
- For multi-sheet visualizations, consider using subplots or combining data

Return ONLY the Python code, no explanations or markdown formatting. The code should be executable as-is.
"""
        
        try:
            response = self.model.generate_content(prompt)
            code = self._extract_code(response.text)
            return code
        except Exception as e:
            raise Exception(f"Error generating chart code with Gemini: {str(e)}")
    
    def generate_answer_from_result(self, question: str, result: Any) -> str:
        """Generate a natural language answer from the query result"""
        result_str = str(result)
        
        prompt = f"""User asked: {question}

The data analysis returned: {result_str}

Provide a clear, concise answer to the user's question based on this result. Be conversational and helpful.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback to simple formatting
            return f"Based on the data: {result_str}"

