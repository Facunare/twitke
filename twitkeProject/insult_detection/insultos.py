import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

data = pd.read_csv('dataset.csv')

train_data, test_data, train_labels, test_labels = train_test_split(data['frase'], data['tipo'], test_size=0.2, random_state=42)

tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(train_data)
tokenizer_json = tokenizer.to_json()
with open('tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(tokenizer_json)
train_sequences = tokenizer.texts_to_sequences(train_data)
test_sequences = tokenizer.texts_to_sequences(test_data)

max_seq_length = max(len(seq) for seq in train_sequences)
train_sequences = pad_sequences(train_sequences, maxlen=max_seq_length)
test_sequences = pad_sequences(test_sequences, maxlen=max_seq_length)

model = Sequential()
model.add(Embedding(10000, 128, input_length=max_seq_length))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

historial = model.fit(train_sequences, train_labels, epochs=200, batch_size=16)

loss, accuracy = model.evaluate(test_sequences, test_labels)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

model.save('model.h5')

new_texts = ["sadasdsads", "hijo de puta"]
new_sequences = tokenizer.texts_to_sequences(new_texts)
new_sequences = pad_sequences(new_sequences, maxlen=max_seq_length)

predictions = model.predict(new_sequences)
for text, prediction in zip(new_texts, predictions):
    if prediction >= 0.5:
        print(f'Frase: {text}, Tipo: Insulto')
    else:
        print(f'Frase: {text}, Tipo: No insulto')
