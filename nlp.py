import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
from textblob import TextBlob
from transformers import pipeline

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Cargar datos
df = pd.read_csv('text_data.csv')

# Función de preprocesamiento
def preprocess_text(text):
    text = text.lower()  # Convertir a minúsculas
    text = re.sub(f"[{string.punctuation}]", "", text)  # Eliminar puntuación
    text = re.sub("\\s+", " ", text).strip()  # Eliminar espacios adicionales
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)

df['clean_text'] = df['text'].apply(preprocess_text)

# Bag of Words (BoW)
vectorizer = CountVectorizer()
bow_matrix = vectorizer.fit_transform(df['clean_text'])

# TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['clean_text'])

# Word Embeddings con Word2Vec
sentences = [sentence.split() for sentence in df['clean_text']]
word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# Análisis de sentimiento con TextBlob
df['sentiment_textblob'] = df['clean_text'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Análisis de sentimiento con modelo preentrenado de transformers
sentiment_pipeline = pipeline('sentiment-analysis')
df['sentiment_transformers'] = df['clean_text'].apply(lambda x: sentiment_pipeline(x)[0]['label'])

print("Preprocesamiento y análisis NLP completados.")
