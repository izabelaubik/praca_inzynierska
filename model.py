from transformers import BertForSequenceClassification, BertTokenizer
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset
from transformers import TrainingArguments, Trainer
import torch
import numpy as np

def predict(x_predict):
    model_name = "bert-base-cased"

    model_path = "D:\label2\checkpoint-15000"
    print("1")
    print("2")
    tokenizer = BertTokenizer.from_pretrained(model_name)
    print("3")

    model = BertForSequenceClassification.from_pretrained(model_path)

    print("4")

    class CustomDataset(Dataset):
        def __init__(self, encodings, labels=None):
            self.encodings = encodings
            self.labels = labels.values if labels is not None else None

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            if self.labels is not None:
                item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.encodings["input_ids"])

    print("5")

    x_predict_tokenized = tokenizer(x_predict, padding=True, truncation=True, max_length=512)
    print("6")

    x_dataset = CustomDataset(x_predict_tokenized)
    print("7")

    raw_pred, _, _ = Trainer(model).predict(x_dataset)
    print("8")

    predictions = np.argmax(raw_pred, axis=1)
    print("9")
    predictions = np.where(predictions == 1, 'positive', 'negative')


    print(predictions)
    return predictions