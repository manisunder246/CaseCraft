# 1. Extracting PART I data into MLX format
# import fitz  # PyMuPDF
# import re
# import json

# # Path to the PDF and output JSONL file
# input_pdf_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/LEGAL FRAMEWORK/ACT/IBC_act_2016.pdf"
# output_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/LEGAL FRAMEWORK/ACT/part1_extracted.jsonl"

# # Patterns for extraction
# part_pattern = re.compile(r"^(PART I)\b", re.IGNORECASE)  # Detects PART I
# section_pattern = re.compile(r"^(\d+)\.\s+(.+?)\s*-", re.UNICODE)  # Matches "1. Short title, extent and commencement -"
# separator_pattern = re.compile(r"^_{5,}$")  # Detects horizontal separator (like a line)
# footnote_pattern = re.compile(r"^\d+\s")  # Matches footnotes like "1 Some text..."

# # Load the PDF
# doc = fitz.open(input_pdf_path)

# # Variables to store extracted data
# current_section = None
# current_text = []
# sections = []
# extracting = False  # Flag to check if we are inside PART I
# current_part = "PART I"
# current_chapter = "PRELIMINARY"
# inside_footnotes = False  # Flag to detect if we are inside footnotes

# for page in doc:
#     text = page.get_text("text").strip()
#     lines = text.split("\n")

#     for line in lines:
#         line = line.strip()

#         # Detect start of PART I
#         if part_pattern.match(line):
#             extracting = True
#             continue  # Skip this line

#         # Stop extracting when reaching PART II
#         if "PART II" in line:
#             extracting = False
#             break  # Exit loop

#         if extracting:
#             # Detect horizontal separator (footnotes usually start after this)
#             if separator_pattern.match(line):
#                 inside_footnotes = True  # Mark footnote section but do nothing
#                 continue

#             # Ignore footnotes entirely
#             if inside_footnotes or footnote_pattern.match(line):
#                 continue

#             # Check for section heading (e.g., "1. Short title, extent and commencement -")
#             section_match = section_pattern.match(line)
#             if section_match:
#                 # Save the previous section if it exists
#                 if current_section and current_text:
#                     sections.append({
#                         "text": f"{current_part} - {current_chapter} - {current_section}: {' '.join(current_text)}"
#                     })

#                 # Start new section
#                 current_section = f"Section {section_match.group(1)}. {section_match.group(2).strip()}"
#                 current_text = [line.split("-")[-1].strip()]  # Store text after the title
#             else:
#                 # Append text to current section
#                 if current_section:
#                     current_text.append(line.replace("\u201c", '"').replace("\u201d", '"'))

# # Save the last section
# if current_section and current_text:
#     sections.append({
#         "text": f"{current_part} - {current_chapter} - {current_section}: {' '.join(current_text)}"
#                 .replace("\u201c", '"').replace("\u201d", '"')  # Fixing quote encoding
#     })

# # Write to JSONL file
# with open(output_jsonl_path, "w", encoding="utf-8") as f:
#     for entry in sections:
#         f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# print(f"✅ Extraction complete. PART I data saved at: {output_jsonl_path}")



#2. FULL doc extraction into MLX format
import fitz  # PyMuPDF
import re
import json

# Path to the PDF and output JSONL file
input_pdf_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/LEGAL FRAMEWORK/ACT/IBC_act_2016.pdf"
output_jsonl_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/LEGAL FRAMEWORK/ACT/full_extracted.jsonl"

# Patterns for extraction
part_pattern = re.compile(r"^(PART\s+[IVXLCDM]+)\b", re.IGNORECASE)  # Detects PART #
chapter_pattern = re.compile(r"^(CHAPTER\s+[IVXLCDM]+)\b", re.IGNORECASE)  # Detects CHAPTER #
section_pattern = re.compile(r"^(\d+)\.\s+(.+?)\s*-", re.IGNORECASE)  # Detects "1. Section Title -"
separator_pattern = re.compile(r"^_{5,}$")  # Detects horizontal separator (like a line)
footnote_pattern = re.compile(r"^\d+\s")  # Matches footnotes like "1 Some text..."

# Load the PDF
doc = fitz.open(input_pdf_path)

# Variables to store extracted data
current_part = None
current_part_name = []
current_chapter = None
current_chapter_name = []
current_section = None
current_text = []
sections = []
inside_footnotes = False  # Flag to track footnote section
first_chapter_in_part = False
ignore_part_I = True  # Flag to ignore PART I

for page in doc:
    text = page.get_text("text").strip()
    lines = text.split("\n")

    for i, line in enumerate(lines):
        line = line.strip()

        # Detect PART (Ignore PART I)
        part_match = part_pattern.match(line)
        if part_match:
            part_number = part_match.group(1)
            if part_number == "PART I":  # Skip everything until PART II
                current_part = None
                continue
            if part_number == "PART II":
                ignore_part_I = False  # Start extracting from PART II

            if ignore_part_I:
                continue  # Still skipping PART I

            if current_section and current_text:
                sections.append({
                    "text": f"{current_part} ({' '.join(current_part_name)}), {current_chapter} ({' '.join(current_chapter_name)}), {current_section}, {' '.join(current_text)}"
                })

            current_part = part_number
            current_part_name = [lines[i + 1].strip()] if i + 1 < len(lines) else []
            current_chapter = None
            current_chapter_name = []
            first_chapter_in_part = True
            continue

        # Capture multi-line PART name
        if current_part and not current_chapter and len(current_part_name) < 2 and line:
            current_part_name.append(line)
            continue

        # Detect CHAPTER
        chapter_match = chapter_pattern.match(line)
        if chapter_match:
            if ignore_part_I:
                continue  # Skip PART I content

            if current_section and current_text:
                sections.append({
                    "text": f"{current_part} ({' '.join(current_part_name)}), {current_chapter} ({' '.join(current_chapter_name)}), {current_section}, {' '.join(current_text)}"
                })

            current_chapter = chapter_match.group(1)
            current_chapter_name = [lines[i + 1].strip()] if i + 1 < len(lines) else []
            current_section = None
            current_text = []
            first_chapter_in_part = False
            continue

        # Capture multi-line CHAPTER name
        if current_chapter and not current_section and len(current_chapter_name) < 2 and line:
            current_chapter_name.append(line)
            continue

        # Detect horizontal separator (footnotes usually start after this)
        if separator_pattern.match(line):
            inside_footnotes = True  # Mark footnote section but do nothing
            continue

        # Ignore footnotes entirely
        if inside_footnotes or footnote_pattern.match(line):
            continue

        # Detect Section Heading (e.g., "1. Section Title -")
        section_match = section_pattern.match(line)
        if section_match:
            if ignore_part_I:
                continue  # Skip PART I content

            # Save previous section if exists
            if current_section and current_text:
                sections.append({
                    "text": f"{current_part} ({' '.join(current_part_name)}), {current_chapter} ({' '.join(current_chapter_name)}), {current_section}, {' '.join(current_text)}"
                })

            # Start new section
            current_section = f"Section {section_match.group(1)}. {section_match.group(2).strip()}"
            current_text = [line.split("-")[-1].strip()]  # Store text after the title
        else:
            # Append text to current section
            if current_section:
                current_text.append(line)

# Save the last section
if current_section and current_text:
    sections.append({
        "text": f"{current_part} ({' '.join(current_part_name)}), {current_chapter} ({' '.join(current_chapter_name)}), {current_section}, {' '.join(current_text)}"
    })

# Write to JSONL file in MLX format
with open(output_jsonl_path, "w", encoding="utf-8") as f:
    for entry in sections:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"✅ Extraction complete. Full document saved at: {output_jsonl_path}")






