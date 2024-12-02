import pandas as pd
import json

# Load the Excel file (update the file path)
file_path = "hello.xlsx"
df = pd.read_excel(file_path, header=None)  # No column names, so header=None

# Save each question as a line in a JSONL file
output_file = "new_dataset.jsonl"
with open(output_file, "w") as file:
    for _, row in df.iterrows():
        json.dump({"question_number": row[0], "code": ""}, file)
        file.write("\n")

print(f"JSONL file saved to {output_file}.")
