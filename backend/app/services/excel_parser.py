import pandas as pd
import os
from typing import Dict, Any, List
import openpyxl
import xlrd


class ExcelParser:
    @staticmethod
    def parse_excel(file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Parse Excel file and return dictionary of sheet_name -> DataFrame
        Supports both .xlsx and .xls formats
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.xlsx':
            excel_file = pd.ExcelFile(file_path, engine='openpyxl')
        elif file_ext == '.xls':
            excel_file = pd.ExcelFile(file_path, engine='xlrd')
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        dataframes = {}
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            # Remove completely empty rows and columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            dataframes[sheet_name] = df
        
        return dataframes
    
    @staticmethod
    def extract_schema_info(dataframes: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        """
        Extract schema information from dataframes for AI context
        Returns dictionary with sheet_name -> schema info
        """
        schema_info = {}
        
        for sheet_name, df in dataframes.items():
            if df.empty:
                continue
            
            # Get column info
            columns = df.columns.tolist()
            dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
            
            # Get sample rows (first 3 non-null rows)
            sample_rows = []
            for idx, row in df.head(5).iterrows():
                sample_row = {}
                for col in columns:
                    val = row[col]
                    # Convert non-serializable types
                    if pd.isna(val):
                        sample_row[col] = None
                    elif isinstance(val, (pd.Timestamp, pd.DatetimeTZDtype)):
                        sample_row[col] = str(val)
                    else:
                        sample_row[col] = val
                sample_rows.append(sample_row)
            
            # Basic statistics
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            stats = {}
            if numeric_cols:
                stats = df[numeric_cols].describe().to_dict()
                # Convert to serializable format
                for col in stats:
                    stats[col] = {k: float(v) if pd.notna(v) else None 
                                 for k, v in stats[col].items()}
            
            schema_info[sheet_name] = {
                "columns": columns,
                "dtypes": dtypes,
                "row_count": len(df),
                "sample_rows": sample_rows,
                "numeric_columns": numeric_cols,
                "statistics": stats
            }
        
        return schema_info

