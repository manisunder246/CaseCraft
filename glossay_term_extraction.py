# # 1. Legal Glossary extraction to jsonl format
# import os
# import json
# import pandas as pd

# # Path to the Excel file and output JSONL file
# input_excel_path = '/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/glossary.xlsx'
# output_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train_1.jsonl"

# def convert_glossary_to_jsonl(input_excel_path, output_jsonl_path):
#     # Load all sheets from the Excel file
#     sheets = pd.read_excel(input_excel_path, sheet_name=None)  # Load all sheets

#     with open(output_jsonl_path, 'w', encoding='utf-8') as jsonl_file:
#         for sheet_name, df in sheets.items():
#             # Drop rows with NaN values
#             df.dropna(subset=["legal term", "meaning"], inplace=True)

#             # Iterate through each row and write to JSONL
#             for _, row in df.iterrows():
#                 entry = {"text": f"{row['legal term']}: {row['meaning']}"}
#                 jsonl_file.write(json.dumps(entry) + "\n")

#     print(f"All sheets converted into MLX-compatible format: '{output_jsonl_path}'")

# # Run the conversion
# convert_glossary_to_jsonl(input_excel_path, output_jsonl_path)

# #2. IBC glossary extraction to jsonl format
# import os
# import json
# import re
# import docx

# # Paths
# input_docx_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/IBC Glossary.docx"
# output_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train_2.jsonl"

# # Load the .docx file
# doc = docx.Document(input_docx_path)
# text_lines = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# # Patterns to detect glossary entries and section headers
# entry_pattern = re.compile(r"\((\d+[A-Z]*)\)\s*\“([^”]+)\”")  # Matches (23) "term" and (23D) "term"
# section_pattern = re.compile(r"(PART I: Definitions|PART II: Definitions|PART III: Definitions)", re.IGNORECASE)
# explanation_pattern = re.compile(r"\bExplanation\b[:\s]*(.*)", re.IGNORECASE)

# # Section mappings (ensuring exact match)
# sections = ["PART I: Definitions", "PART II: Definitions", "PART III: Definitions"]
# current_section = None
# section_wise_entries = {section: [] for section in sections}
# glossary_entries = []
# current_term = None
# current_definition = []

# for line in text_lines:
#     # Detect if a new section starts
#     section_match = section_pattern.match(line)
#     if section_match:
#         current_section = section_match.group(1)  # Extract the exact section name
#         continue  # Skip to the next line

#     # Ensure we are inside a valid section
#     if current_section is None:
#         continue  # Ignore text outside of the predefined sections

#     # Check if line starts a new glossary term (Numbered format: (12) "term" means ...)
#     match = entry_pattern.match(line)
#     if match:
#         # Store the previous term before starting a new one
#         if current_term and current_definition:
#             entry = {"text": f"{current_term}: {' '.join(current_definition)}"}
#             section_wise_entries[current_section].append(entry)
#             glossary_entries.append(entry)

#         # Start a new term extraction
#         current_term = match.group(2)  # Extract term inside quotes
#         current_definition = [line.split("”")[-1].strip()]  # Capture definition after the term
    
#     elif current_term:
#         # Continue adding lines to the current term's definition
#         explanation_match = explanation_pattern.match(line)
#         if explanation_match:
#             current_definition.append(f"Explanation: {explanation_match.group(1).strip()}")
#         else:
#             current_definition.append(line.strip())

# # Save the last entry
# if current_term and current_definition:
#     entry = {"text": f"{current_term}: {' '.join(current_definition)}"}
#     section_wise_entries[current_section].append(entry)
#     glossary_entries.append(entry)

# # Write to JSONL file
# with open(output_jsonl_path, "w", encoding="utf-8") as f:
#     for entry in glossary_entries:
#         f.write(json.dumps(entry) + "\n")

# # Print section-wise word counts
# print("\n✅ Section-wise extraction results:")
# total_count = 0
# for section, entries in section_wise_entries.items():
#     count = len(entries)
#     total_count += count
#     print(f"{section}: {count} terms")

# print(f"\n✅ Total terms extracted: {total_count}")
# print(f"✅ Final JSONL file saved at: '{output_jsonl_path}'")

# 3. Merging the above 2 codes.
# import os
# import json
# import re
# import docx
# import pandas as pd

# # Paths
# input_docx_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/IBC Glossary.docx"
# input_excel_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/glossary.xlsx"
# output_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train.jsonl"

# # Load the .docx file
# doc = docx.Document(input_docx_path)
# text_lines = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# # Patterns to detect glossary entries and section headers
# entry_pattern = re.compile(r"\((\d+[A-Z]*)\)\s*\“([^”]+)\”")  # Matches (23) "term" and (23D) "term"
# section_pattern = re.compile(r"(PART I: Definitions|PART II: Definitions|PART III: Definitions)", re.IGNORECASE)
# explanation_pattern = re.compile(r"\bExplanation\b[:\s]*(.*)", re.IGNORECASE)

# # Section mappings (ensuring exact match)
# sections = ["PART I: Definitions", "PART II: Definitions", "PART III: Definitions"]
# current_section = None
# section_wise_entries = {section: [] for section in sections}
# glossary_entries = []
# current_term = None
# current_definition = []

# for line in text_lines:
#     # Detect if a new section starts
#     section_match = section_pattern.match(line)
#     if section_match:
#         current_section = section_match.group(1)  # Extract the exact section name
#         continue  # Skip to the next line

#     # Ensure we are inside a valid section
#     if current_section is None:
#         continue  # Ignore text outside of the predefined sections

#     # Check if line starts a new glossary term (Numbered format: (12) "term" means ...)
#     match = entry_pattern.match(line)
#     if match:
#         # Store the previous term before starting a new one
#         if current_term and current_definition:
#             entry = {"text": f"{current_term}: {' '.join(current_definition)}"}
#             section_wise_entries[current_section].append(entry)
#             glossary_entries.append(entry)

#         # Start a new term extraction
#         current_term = match.group(2)  # Extract term inside quotes
#         current_definition = [line.split("”")[-1].strip()]  # Capture definition after the term
    
#     elif current_term:
#         # Continue adding lines to the current term's definition
#         explanation_match = explanation_pattern.match(line)
#         if explanation_match:
#             current_definition.append(f"Explanation: {explanation_match.group(1).strip()}")
#         else:
#             current_definition.append(line.strip())

# # Save the last entry
# if current_term and current_definition:
#     entry = {"text": f"{current_term}: {' '.join(current_definition)}"}
#     section_wise_entries[current_section].append(entry)
#     glossary_entries.append(entry)

# # Load all sheets from the Excel file
# sheets = pd.read_excel(input_excel_path, sheet_name=None)  # Load all sheets

# for sheet_name, df in sheets.items():
#     # Drop rows with NaN values
#     df.dropna(subset=["legal term", "meaning"], inplace=True)

#     # Iterate through each row and write to JSONL
#     for _, row in df.iterrows():
#         entry = {"text": f"{row['legal term']}: {row['meaning']}"}
#         glossary_entries.append(entry)

# # Write to JSONL file
# with open(output_jsonl_path, "w", encoding="utf-8") as f:
#     for entry in glossary_entries:
#         f.write(json.dumps(entry) + "\n")

# # Print section-wise word counts
# print("\n✅ Section-wise extraction results:")
# total_count = 0
# for section, entries in section_wise_entries.items():
#     count = len(entries)
#     total_count += count
#     print(f"{section}: {count} terms")

# print(f"\n✅ Total terms extracted: {total_count}")
# print(f"✅ Final JSONL file saved at: '{output_jsonl_path}'")

# 4. Preparing test and valid files:
import os
import json
import random

# Paths
input_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train_split.jsonl"
train_output_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/train.jsonl"
valid_output_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/valid.jsonl"
test_output_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/Glossary/data/test.jsonl"

# Load data
with open(input_jsonl_path, "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

# Shuffle data to ensure randomness
random.shuffle(data)

# Compute split sizes
total_count = len(data)
train_size = int(0.7 * total_count)
valid_size = int(0.2 * total_count)
test_size = total_count - train_size - valid_size  # Ensuring all data is used

# Split data
train_data = data[:train_size]
valid_data = data[train_size:train_size + valid_size]
test_data = data[train_size + valid_size:]

# Write new train.jsonl
with open(train_output_path, "w", encoding="utf-8") as f:
    for entry in train_data:
        f.write(json.dumps(entry) + "\n")

# Write valid.jsonl
with open(valid_output_path, "w", encoding="utf-8") as f:
    for entry in valid_data:
        f.write(json.dumps(entry) + "\n")

# Write test.jsonl
with open(test_output_path, "w", encoding="utf-8") as f:
    for entry in test_data:
        f.write(json.dumps(entry) + "\n")

# Print counts
print(f"✅ Data split completed:")
print(f"- Training: {len(train_data)} entries")
print(f"- Validation: {len(valid_data)} entries")
print(f"- Test: {len(test_data)} entries")
print(f"✅ Files saved:")
print(f"- Train: {train_output_path}")
print(f"- Validation: {valid_output_path}")
print(f"- Test: {test_output_path}")


