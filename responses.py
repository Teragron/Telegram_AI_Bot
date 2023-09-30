from datetime import datetime

import nltk
from snowballstemmer import TurkishStemmer
from keras.models import Sequential
from keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np
import pandas as pd
import numpy
import random
import json
import requests
import csv
from kripto import *

moviestemp = []

with open("movies.csv", 'r') as file:
    reader = csv.reader(file, delimiter = '\t', skipinitialspace=True)
    for row in reader:
        moviestemp.append(row[0])
    
movies = []

for i in moviestemp:
    a = i.split(",")
    movies.append(a[1])
    
    
    
    

api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"


with open("corpusyedek.json", encoding='utf-8') as file:
    data = json.load(file)
    
with open("world-cities.json", encoding='utf-8') as file:
    sehir = json.load(file)
    
sehirler = []
for i in sehir:
    sehirler.append(i["name"].lower())

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


from keras.models import load_model
# returns a compiled model
# identical to the previous one
model = load_model('my_model1.h5')


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stemWord(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

wut = ["Tam olarak anlayamadım", "Tekrar eder misin?", "Duyamadim tekrar söyler misin?", "af buyur"]



def sample_responses(input_text):
    
    list1=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    b = random.randint(0,7)
    c = random.randint(0,7)
    randomfoto = "https://picsum.photos/seed/{}{}/1920/1080".format(list1[b],list1[c])
    
    user_message = str(input_text).lower()
    
    results = model.predict(np.asanyarray([bag_of_words(input_text, words)]))[0]
    
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    
    if results[results_index] > 0.85:
        
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                if tag == "saat":
                    now = datetime.now()
                    date_time = now.strftime("%d/%m/%y, %H:%M:%S")
                    return str(date_time)
                if tag == "foto":
                    return randomfoto
                if tag == "filmtavsiye":
                    return movies[random.randrange(1000)]

        return random.choice(responses)
    
    
    
    if "hava" in user_message.split() or "derece" in user_message.split():
        idx = user_message.split().index(list(set(user_message.split()) & set(sehirler))[0])
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(user_message.split()[idx],api_key)
        response = requests.get(url)
        datam = json.loads(response.text)
        hava = str(datam["main"]["temp"]-273.15) + " Derece"
        print(bool(set(user_message.split()) & set(sehirler)))
        return hava
    
    if user_message in ("foto", "at", "fotoğraf","resim","görsel"):
        return randomfoto
    if "film" in user_message:
        return movies[random.randrange(1000)]
    if user_message in ("Merhabalar", "Selamlar", "Nasılsın", "Naber", "Selam","Günaydın", "napıyon", "nasılsın", "selam", "merhaba"):
        return "selam naber?"
    if user_message.split()[-1] in ("kadar","fiyat", "fiyatı", "kadar?", "fiyatı?", "fiyat?", "para"):
        if user_message.split()[0].isdigit():
            xi = int(user_message.split()[0])
            zip(*symbols)
            column1, column2 = zip(*symbols)
            if user_message.split()[1] in column1:
                for idx,j in enumerate(column1):
                    if j ==  user_message.split()[1]:
                        return str(xi*get_current_data((column2[idx]))["USD"]) + " dolar"
        else:
            zip(*symbols)
            column1, column2 = zip(*symbols)
            if user_message.split()[0] in column1:
                for idx,j in enumerate(column1):
                    if j ==  user_message.split()[0]:
                        return str(get_current_data((column2[idx]))["USD"]) + " dolar"
    return "I don't understand it."
