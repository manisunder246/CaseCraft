# #1. Inspect the contents of the updated weights
# import numpy as np

# adapter_path = "mlx-examples/lora/adapters.npz"  # Ensure the correct path
# data = np.load(adapter_path, allow_pickle=True)

# print(data.files)  # Lists all stored variables

#2. Testing the fusion

import mlx.core as mx

model_path = "/Users/manisunder/Desktop/DEGREES & CERTS/MTECH/AI-ML/SEM-4/Dissertation/CaseCraft/DATA/FINETUNED MODEL/model.safetensors.index.json"

try:
    model_weights = mx.load(model_path)
    print(f"✅ Successfully loaded fused model with {len(model_weights)} parameters.")
except Exception as e:
    print(f"❌ Failed to load fused model: {e}")

