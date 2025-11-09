import os
import pandas as pd
from datetime import datetime

class ExcelLogger:
    def __init__(self, log_dir="reports", filename="test_results.xlsx"):
        self.log_dir = log_dir
        self.filename = filename
        os.makedirs(log_dir, exist_ok=True)
        self.file_path = os.path.join(log_dir, filename)

        # If file doesn’t exist, create it with headers
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=[
                "Timestamp", "Module", "Test Case ID", "Description", "Status", "Error Message"
            ])
            df.to_excel(self.file_path, index=False)

    def log(self, module, tc_id, desc, status, error=""):
        """Append a new test log entry to Excel file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
            "Timestamp": timestamp,
            "Module": module,
            "Test Case ID": tc_id,
            "Description": desc,
            "Status": status,
            "Error Message": error,
        }

        # Read old data if available
        df = pd.read_excel(self.file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Save updated file
        df.to_excel(self.file_path, index=False)
        print(f"[LOG] {tc_id} - {status}")

    def get_log_file(self):
        """Return full path of Excel log file."""
        return os.path.abspath(self.file_path)
