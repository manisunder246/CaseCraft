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

## 🔧 **Modifications in mlx-examples Repository**

To adapt the **mlx-finetuning** process for our requirements, I modified a few files, making key adjustments for **training, logging, and model handling**.

### 📝 **1. `lora.py` - Fine-Tuning Enhancements**

#### **Added WandB Integration**
Integrated **Weights & Biases (WandB)** to track fine-tuning progress and visualize metrics.

```python
import wandb
wandb.init(project="mlx-finetuning", name="LoRA_Training")
```

Logged **training and validation metrics** dynamically:
```python
wandb.log({"train_loss": loss, "val_loss": val_loss})
```

Configured **hyperparameter tracking**:
```python
wandb.config.update({
    "learning_rate": args.learning_rate,
    "batch_size": args.batch_size,
    "epochs": args.iters
})
```

#### **Added Custom Adapter Saving**
Specified **custom paths for saving adapter weights**:
```python
adapter_save_path = "./trained_adapters/"
os.makedirs(adapter_save_path, exist_ok=True)
```
Saved **adapter weights in `safetensors` format**:
```python
mx.savez(f"{adapter_save_path}/adapters.safetensors", **dict(tree_flatten(model.trainable_parameters())))
```
Defined **detailed adapter configurations for LoRA**:
```python
adapter_config = {
    "rank": 16,
    "scaling": 20.0,
    "dropout": 0.05
}
```

### 📝 **2. `utils.py` - Enhanced Model Loading**

#### **Modified Model Loading to Support Nested `text_config`**
Added **support for handling multimodal models like LLaMA 3.2 Vision**:
```python
if "text_config" in model_config:
    model_config.update(model_config["text_config"])
```
This ensures **compatibility with hybrid text-vision architectures**, making the fine-tuning process adaptable for diverse use cases.

---

