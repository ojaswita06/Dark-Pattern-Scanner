import pandas as pd
import numpy as np

from datasets import Dataset

from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from config import *

#loading validation data
val_df = pd.read_csv(VAL_PATH)

dataset = Dataset.from_pandas(val_df)

tokenizer = BertTokenizer.from_pretrained(MODEL_SAVE_PATH)

def tokenize(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH
    )

dataset = dataset.map(tokenize, batched=True)

dataset = dataset.rename_column("label", "labels")

dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

model = BertForSequenceClassification.from_pretrained(
    MODEL_SAVE_PATH
)

trainer = Trainer(model=model)

predictions = trainer.predict(dataset)

preds = np.argmax(predictions.predictions, axis=1)
labels = predictions.label_ids

accuracy = accuracy_score(labels, preds)
precision = precision_score(
    labels,
    preds,
    average="weighted"
)

recall = recall_score(
    labels,
    preds,
    average="weighted"
)

f1 = f1_score(
    labels,
    preds,
    average="weighted"
)

cm = confusion_matrix(labels, preds)

print("\n=== RESULTS ===")
print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nConfusion Matrix")
print(cm)

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()

plt.title("Dark Pattern Classifier Confusion Matrix")

plt.savefig("confusion_matrix.png")

plt.show()