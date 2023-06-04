import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json

class InsultDetector:
    def __init__(self, model_path, tokenizer_path, max_seq_length):
        self.model = load_model(model_path)
        with open(tokenizer_path) as f:
            data = f.read()
            self.tokenizer = tokenizer_from_json(data)
        self.max_seq_length = max_seq_length

    def preprocess_text(self, text):
        sequences = self.tokenizer.texts_to_sequences([text])
        sequences = pad_sequences(sequences, maxlen=self.max_seq_length)
        return sequences

    def classify_text(self, text):
        sequences = self.preprocess_text(text)
        prediction = self.model.predict(sequences)[0][0]
        return prediction
