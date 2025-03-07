#1. fixing the json files
import json

input_file = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train.jsonl"
output_file = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train_fixed.jsonl"

# Read the JSON file
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)  # Load as a full JSON object (list of dicts)

# Ensure it's a list of dictionaries
if isinstance(data, list):
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in data:
            if isinstance(entry, dict):  # Ensure valid entries
                f.write(json.dumps(entry) + "\n")  # Write each dict as a separate line

print(f"Fixed JSONL saved as: {output_file}")
