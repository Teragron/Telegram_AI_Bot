import nltk
from snowballstemmer import TurkishStemmer
from keras.models import Sequential
from keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import AdamW
import numpy as np
import pandas as pd
import numpy
import random
import json

import wandb
from wandb.keras import WandbMetricsLogger

wandb.login()

wandb.init(config={"bs": my_epoch})

my_epoch = 200
my_lr = 0.001




with open("corpus.json", encoding='utf-8') as file:
    data = json.load(file)


stemmer=TurkishStemmer()
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stemWord(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []
out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stemWord(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
print(np.shape(training))
output = numpy.array(output)
print(np.shape(output))

model = Sequential()
model.add(Dense(64,input_shape=(len(training[0]),),activation="relu"))
model.add(Dense(32,activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(47,activation="softmax"))
model.summary()
model.compile(AdamW(learning_rate=my_lr),loss="categorical_crossentropy",metrics=["accuracy"])
model.fit(training, output,epochs=my_epoch, verbose=2,batch_size=128, callbacks=[WandbMetricsLogger()])


from keras.models import load_model

model.save('my_model.h5') 
