import pandas as pd
from sklearn.model_selection import train_test_split

df=pd.read_csv("data/raw/dataset.tsv", sep="\t")

df=df[["text", "Pattern Category"]]

df=df.drop_duplicates()

valid_classes = [
    "Not Dark Pattern",
    "Scarcity",
    "Social Proof",
    "Urgency",
    "Misdirection"
]

df = df[
    df["Pattern Category"].isin(valid_classes)
]

label_mapping={
    "Not Dark Pattern": 0,
    "Scarcity": 1,
    "Social Proof": 2,
    "Urgency": 3,
    "Misdirection": 4
}

df["label"]= df["Pattern Category"].map(label_mapping)

train_df, temp_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.5,
    random_state=42,
    stratify=temp_df["label"]
)

train_df.to_csv(
    "data/processed/train.csv",
    index= False
)

val_df.to_csv(
    "data/processed/val.csv",
    index= False
)

test_df.to_csv(
    "data/processed/test.csv",
    index= False
)

print("Preprocessing Complete")
print(f"Train Size: {len(train_df)}")
print(f"Validation Size: {len(val_df)}")
print(f"Test Size: {len(test_df)}")

