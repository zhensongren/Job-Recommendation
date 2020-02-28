from flask import Flask, render_template, request
import re 
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def classify(text, preprocessor, model):

	corpus = []
	text = re.sub('[^a-zA-Z]', ' ', text)
	text = text.lower()
	text = text.split()
	lemmatizer = WordNetLemmatizer()
	text = [lemmatizer.lemmatize(word) for word in text if not word in set(stopwords.words('english'))]
	text = ' '.join(text)
	corpus.append(text)
	

	x_tfid = preprocessor.transform(corpus).toarray()
	answer = model.predict(x_tfid)
	answer = str(answer[0])
	
	if answer == '0':
		return "You are very likely applying a Machine Learning Engineer Position."
	elif answer == '1':
		return "You are very likely applying a Data Scientist Position."
	elif answer == '2':
		return "You are very likely applying a Data Engineer Position."
	else:
		return "You are very likely applying a Data Analyst Position."
