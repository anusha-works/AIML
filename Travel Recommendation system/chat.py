import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import pickle

# Load data from the JSON file
with open('intents.json') as file:
    data = json.load(file)

# Extract patterns and responses
patterns = []
responses = []
for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        responses.append(intent['tag'])

# Encode the responses
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(responses)

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(patterns)


# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(tfidf_matrix, labels, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier

# Create and train a RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=100)
classifier.fit(X_train, y_train)

# Predict the intent
predictions = classifier.predict(X_test)

def chatbot(user_input):
    # Preprocess user input using the same TF-IDF vectorizer
    input_vector = tfidf_vectorizer.transform([user_input])

    # Predict the intent
    predicted_label = classifier.predict(input_vector)[0]

    # Get the response based on the predicted label
    response = random.choice([intent['responses'] for intent in data['intents'] if label_encoder.transform([intent['tag']])[0] == predicted_label])
    res = random.choice(response)
    return res
