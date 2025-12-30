import json
import pandas as pd
from typing import Dict, Any
import plotly.graph_objects as go
import plotly.express as px


class ChartGenerator:
    @staticmethod
    def execute_chart_code(code: str, dataframes: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Execute chart generation code in a safe context
        Returns the chart JSON
        """
        # Create a safe execution context
        safe_globals = {
            'pd': pd,
            'dataframes': dataframes,
            'go': go,
            'px': px,
            'plotly': __import__('plotly'),
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                '__import__': __import__,
            }
        }
        
        try:
            # Execute the code
            exec(code, safe_globals)
            
            # Get the chart JSON
            if 'chart_json' in safe_globals:
                chart_data = json.loads(safe_globals['chart_json'])
                return chart_data
            elif 'fig' in safe_globals:
                fig = safe_globals['fig']
                if hasattr(fig, 'to_json'):
                    return json.loads(fig.to_json())
                else:
                    raise ValueError("Figure object doesn't have to_json method")
            else:
                raise ValueError("Code did not create 'fig' or 'chart_json' variable")
        
        except Exception as e:
            raise Exception(f"Error executing chart code: {str(e)}")
    
    @staticmethod
    def get_chart_type(chart_data: Dict[str, Any]) -> str:
        """Determine chart type from plotly JSON"""
        if 'data' in chart_data and len(chart_data['data']) > 0:
            trace_type = chart_data['data'][0].get('type', 'unknown')
            type_mapping = {
                'bar': 'bar',
                'scatter': 'line' if chart_data['data'][0].get('mode') == 'lines' else 'scatter',
                'pie': 'pie',
                'histogram': 'histogram',
                'box': 'box',
                'violin': 'violin',
            }
            return type_mapping.get(trace_type, trace_type)
        return 'unknown'

