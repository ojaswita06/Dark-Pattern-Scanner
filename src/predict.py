import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

from src.config import MODEL_SAVE_PATH, MODEL_NAME

# ------------------------
# Load model + tokenizer
# ------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained(MODEL_SAVE_PATH)

model = BertForSequenceClassification.from_pretrained(MODEL_SAVE_PATH)
model.to(device)
model.eval()


# ------------------------
# Label mapping (adjust if needed)
# ------------------------
id2label = {
    0: "NOT_DARK_PATTERN",
    1: "DARK_PATTERN"
}


# ------------------------
# Prediction function
# ------------------------

def predict(text: str):

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
    pred_id = int(np.argmax(probs))

    return {
        "text": text,
        "label": id2label[pred_id],
        "confidence": float(probs[pred_id])
    }


# ------------------------
# Test run
# ------------------------

if __name__ == "__main__":
    sample = "Only 1 item left! Hurry before it sells out!"
    result = predict(sample)
    print(result)