import nltk
nltk.data.path.append('/app')
nltk.download('stopwords', download_dir ='/app')
nltk.download('wordnet', download_dir ='/app')

import joblib
from flask import Flask, render_template, request, redirect
import score
from classify import classify
classifier = joblib.load('indeed_LinearSVC.pkl')
tfidfVectorizer = joblib.load('tfidfVectorizer.pkl')

app = Flask(__name__)

@app.route('/index', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
	if request.method == 'POST':
		# Get the resume from user's input form
		if 'resume' not in request.form:
			return redirect(request.url)
		else:
			resume = request.form['resume']
			
		# Get the job post from user's input form
		if 'job_description' not in request.form:
			return redirect(request.url)
		else:
			job_post = request.form['job_description']

		matching_score = score.get_score(job_post=job_post, resume=resume)
		matching_score = matching_score*100
		matching_score= "{:.0f}".format(matching_score)
		classified_title = classify(job_post, preprocessor= tfidfVectorizer, model=classifier)
		return render_template('home.html',matching_score=matching_score, classified_title=classified_title)
	else:
		return render_template('home.html')
		
if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0", port=5000)
