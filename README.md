# CaseCraft

CaseCraft is an AI-driven legal research tool fine-tuned on **IBC judgments, amendments, and case laws**. It integrates a **custom LLM with a RAG-based retrieval system**, enabling **legal document search, summarization, and Q&A**. This repository includes **fine-tuning scripts, RAG pipeline implementation, and frontend integration**.

## 📂 Project Documentation

### 🐍 Python Files

#### `fine_tuning_llama.py`
A utility script that fixes JSON formatting issues in training data. It reads a JSON file, ensures it contains a **list of dictionaries**, and converts it to a properly formatted **JSONL file** (one JSON object per line) for model fine-tuning.

#### `legal_framework_files_download.py`
An **automated web scraper** that downloads legal framework documents from the **IBBI website**. Uses **Selenium** to navigate through multiple categories (**Acts, Rules, Regulations, etc.**) and download PDFs into organized folders. Includes **dynamic handling of download directories and pagination**.

#### `download_judgments.py`
Similar to the legal framework downloader, this script **automates the downloading of legal judgments** from various courts (**Supreme Court, High Courts, NCLAT, etc.**) from the IBBI website. Uses **Selenium** to handle pagination and organizes downloaded PDFs into **category-specific folders**.

### 📜 Additional Files

#### `LORA_Commands.txt`
Contains command-line instructions for **fine-tuning and fusing a LLaMA model** (creating **"Chanakya"**) using **LoRA (Low-Rank Adaptation)** techniques. Includes commands for:
- Multiple training iterations
- Weight fusion steps
- Embedding extraction

---
