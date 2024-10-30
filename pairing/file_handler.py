import pandas as pd

def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None
