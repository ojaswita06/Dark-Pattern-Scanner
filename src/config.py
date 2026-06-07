MODEL_NAME = "bert-base-uncased"

MAX_LENGTH = 128

BATCH_SIZE = 16

LEARNING_RATE = 2e-5

EPOCHS = 3

NUM_LABELS = 5

TRAIN_PATH = "data/processed/train.csv"
VAL_PATH = "data/processed/val.csv"
TEST_PATH = "data/processed/test.csv"

MODEL_SAVE_PATH = "models/best_model"