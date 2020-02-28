import os
import sys
import click
from flask import Flask, render_template, request, redirect, flash, url_for,session
from flask_sqlalchemy import SQLAlchemy
import score
from sklearn.externals import joblib

from classify import classify

# get_text, PyPDF2

app = Flask(__name__)
classifier = joblib.load('indeed_LinearSVC.pkl')
tfidfVectorizer = joblib.load('tfidfVectorizer.pkl')
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#name = db.Column(db.String(300))
	#location = db.Column(db.String(100))
	resume = db.Column(db.String(5000))


class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#title = db.Column(db.String(60))
	#location = db.Column(db.String(100))
	#post_date = db.Column(db.String(50))
	job_post = db.Column(db.String(5000))
	#link = db.Column(db.String(300))
	#employer = db.Column(db.String(100))
	
	
#Generate fake data
name = 'Zhensong Ren'
jobs = [
{'employer':'Apple', 'title': 'Senior Data Scientist', 'post_date': '08/01/2019', 'link':'				https://jobs.apple.com/en-us/details/200063634/senior-lead-data-scientist'},
{'employer':'Apple', 'title': 'Machine Learning Engineer', 'post_date': '08/01/2019', 'link':'https://jobs.apple.com/en-us/details/200029136/machine-learning-engineer'},
{'employer':'Sam\'s Club', 'title': 'Data Scientist', 'post_date': '08/05/2019', 'link':'https://sjobs.brassring.com/TGnewUI/Search/home/HomeWithPreLoad?PageType=JobDetails&partnerid=25222&siteid=5022&jobid=1408817&codes=Indeed_Organic&utm_source=Indeed_Organic&utm_campaign=eCommerce%2Bwalmartlabs&utm_medium=AppFeeder&utm_term=walmartlabs%2BData_Science_and_Machine_Learning&utm_content=Data_Science_and_Machine_Learning#jobDetails=1408817_5022'},
{'employer':'Shell', 'title': 'Machine Learning Engineer', 'post_date': '08/01/2019', 'link':'https://jobs.shell.com/job/houston/machine-learning-engineer-energy-platform-houston-tx/26631/12744472?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic'},
{'employer':'Verizon', 'title': 'Senior Data Scientist', 'post_date': '08/01/2019', 'link':'http://jobs.verizon.com/jobs/4386284-senior-data-scientist?tm_job=524978-1A&tm_event=view&tm_company=781&bid=538&CID=pst'},
{'employer':'Google', 'title': 'Machine Learning Engineer', 'post_date': '08/08/2019', 'link':'https://careers.google.com/jobs/results/5097432532451328-software-engineer-machine-learning/'},
{'employer':'Facebook', 'title': 'Data Scientist', 'post_date': '08/01/2019', 'link':'https://www.facebook.com/careers/jobs/190268414894537/'},
{'employer':'Microsoft', 'title': 'Senior Data Scientist', 'post_date': '08/09/2019', 'link':'https://careers.microsoft.com/us/en/job/639375/Senior-Data-Scientist'},
{'employer':'Amazon', 'title': 'Data Scientist', 'post_date': '08/04/2019', 'link':'https://www.amazon.jobs/en/jobs/881117/data-scientist-nationwide-opportunities'},
{'employer':'twitter', 'title': 'Machine Learning Engineer', 'post_date': '08/11/2019', 'link':'https://www.linkedin.com/jobs/view/machine-learning-engineer-health-ml-at-twitter-1432967907/?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic'},
]
	
@app.cli.command()
def forge():
	
	db.create_all()
	user = User(name=name)
	for job in jobs:
		job = Job(title=job['title'], link=job['link'])
		#job = Job(title=job['title'], post_date=job['post_date'], employer=job['employer'], link=job['link'], job_post=job['job_post'])
		db.session.add(job)
	db.session.add(user)
	db.session.commit()
	click.echo('Saved the fake data into database.')	

skills = {'access': 'access',
 'algorithm': 'algorithm',
 'algorithms': 'algorithm',
 'amazon': 'amazon',
 'analysis': 'analysis',
 'analytical': 'analysis',
 'analytics': 'analysis',
 'android': 'android',
 'apache': 'apache',
 'api': 'api',
 'arduino': 'arduino',
 'artificial': 'artificial',
 'association': 'association',
 'asteradata': 'asteradata',
 'aws': 'aws',
 'azure': 'azure',
 'bash': 'bash',
 'bayesian': 'bayesian',
 'big': 'big',
 'bootstrap': 'bootstrap',
 'c#': 'c#',
 'c+': 'c+',
 'c++': 'c+',
 'cassandra': 'cassandra',
 'classification': 'classification',
 'cleaning': 'cleaning',
 'cloud': 'cloud',
 'clustering': 'clustering',
 'cnn': 'cnn',
 'cnns': 'cnn',
 'computer': 'computer',
 'computing': 'computer',
 'css': 'css',
 'data': 'data',
 'database': 'database',
 'databases': 'database',
 'db': 'db',
 'ddpg': 'ddpg',
 'decision': 'decision',
 'deep': 'deep',
 'design': 'design',
 'detection': 'detection',
 'development': 'development',
 'distributed': 'distributed',
 'django': 'django',
 'docker': 'docker',
 'dqn': 'dqn',
 'eclipse': 'eclipse',
 'elasticsearch': 'elasticsearch',
 'engineer': 'engineer',
 'etl': 'etl',
 'excel': 'excel',
 'extract': 'extract',
 'flask': 'flask',
 'forest': 'forest',
 'fpga': 'fpga',
 'gans': 'gans',
 'git': 'git',
 'github': 'github',
 'google': 'google',
 'googlevision': 'googlevision',
 'gpu': 'gpu',
 'hadoop': 'hadoop',
 'hbase': 'hbase',
 'hdfs': 'hdfs',
 'hive': 'hive',
 'html': 'html',
 'image': 'image',
 'impala': 'impala',
 'instance': 'instance',
 'intelligence': 'intelligence',
 'java': 'java',
 'javascript': 'javascript',
 'jdbc': 'jdbc',
 'jira': 'jira',
 'jquery': 'jquery',
 'js': 'js',
 'json': 'json',
 'k-nearest': 'k-nearest',
 'kafka': 'kafka',
 'keras': 'keras',
 'kernel': 'kernel',
 'language': 'language',
 'latex': 'latex',
 'learn': 'learn',
 'learning': 'learn',
 'linear': 'linear',
 'linux': 'linux',
 'load': 'load',
 'logistic': 'logistic',
 'lstms': 'lstms',
 'machine': 'machine',
 'management': 'management',
 'mapreduce': 'mapreduce',
 'mathematics': 'mathematics',
 'matlab': 'matlab',
 'matplotlib': 'matplotlib',
 'microsoft': 'microsoft',
 'mining': 'mining',
 'mongodb': 'mongodb',
 'ms': 'ms',
 'multiple': 'multiple',
 'mysql': 'mysql',
 'natural': 'natural',
 'neighbors': 'neighbors',
 'neo': 'neo',
 'net': 'neo',
 'network': 'network',
 'networks': 'network',
 'neural': 'neural',
 'nlp': 'nlp',
 'nltk': 'nltk',
 'node': 'node',
 'nosql': 'nosql',
 'numpy': 'numpy',
 'object': 'object',
 'ocr': 'ocr',
 'ods': 'ods',
 'office': 'office',
 'olap': 'olap',
 'opencv': 'opencv',
 'oracle': 'oracle',
 'pandas': 'pandas',
 'parallel': 'parallel',
 'php': 'php',
 'pl': 'pl',
 'polynomial': 'polynomial',
 'postgressql': 'postgressql',
 'powerbi': 'powerbi',
 'ppo': 'ppo',
 'processing': 'processing',
 'programming': 'programming',
 'pyspark': 'pyspark',
 'python': 'python',
 'pytorch': 'pytorch',
 'random': 'random',
 'react': 'react',
 'redux': 'redux',
 'regression': 'regression',
 'reinforcement': 'reinforcement',
 'rest': 'rest',
 'rnns': 'rnns',
 'sas': 'sas',
 'scala': 'scala',
 'science': 'science',
 'scikit': 'scikit',
 'scikit-learn': 'scikit-learn',
 'scipy': 'scipy',
 'segmentation': 'segmentation',
 'selenium': 'selenium',
 'server': 'server',
 'services': 'services',
 'signal': 'signal',
 'simple': 'simple',
 'software': 'software',
 'spacy': 'spacy',
 'spark': 'spacy',
 'sql': 'sql',
 'ssrs': 'ssrs',
 'statistical': 'statistical',
 'statistics': 'statistical',
 'studio': 'studio',
 'supervised': 'supervised',
 'svm': 'svm',
 'tableau': 'tableau',
 'tensorflow': 'tensorflow',
 'teradata': 'teradata',
 'testing': 'testing',
 'theano': 'theano',
 'tnpg': 'tnpg',
 'tools': 'tools',
 'transform': 'transform',
 'trees': 'trees',
 'trpo': 'trpo',
 'unix': 'unix',
 'unsupervised': 'unsupervised',
 'vba': 'vba',
 'vision': 'vision',
 'visual': 'visual',
 'visualization': 'visualization',
 'web': 'web',
 'xml': 'xml',
 'Python': 'Python',
 'Genism': 'Genism',
 'Statistics': 'Statistics',
 'Pandas': 'Pandas',
 'Git/github': 'Git/github',
 'Image recognition': 'Image recognition',
 'Java': 'Java',
 'NLTK': 'NLTK',
 'Probability': 'Probability',
 'Scikit-learn': 'Scikit-learn',
 'SQL': 'SQL',
 'Natural language processing': 'Natural language processing',
 'Scala': 'Scala',
 'A/B testing': 'A/B testing',
 'TensorFlow': 'TensorFlow',
 'Mongodb': 'Mongodb',
 'speech recognition': 'speech recognition',
 'C++': 'C++',
 'HDFS': 'HDFS',
 'Multivariable Calculus': 'Multivariable Calculus',
 'PyTorch': 'PyTorch',
 'Flask': 'Flask',
 'Language interpretation': 'Language interpretation',
 'MATLAB': 'MATLAB',
 'Hive': 'Hive',
 'Linear Algebra': 'Linear Algebra',
 'Keras': 'Keras',
 'AWS': 'AWS',
 'Autonomous\xa0driving': 'Autonomous\xa0driving',
 'R': 'R',
 'Hadoop': 'Hadoop',
 'Information theory': 'Information theory',
 'CV': 'CV',
 'Linux/Unix': 'Linux/Unix',
 'Recommender System': 'Recommender System',
 'Spark': 'Spark',
 'Real and complex anlysis': 'Real and complex anlysis',
 'NLP': 'NLP',
 'Git': 'Git',
 'Preventive health care': 'Preventive health care',
 'Optimization': 'Optimization',
 'Machine Learning': 'Machine Learning',
 'HTML': 'HTML',
 'Deep Learning': 'Deep Learning',
 'CSS': 'CSS',
 'Numpy': 'Numpy',
 'JavaScript': 'JavaScript',
 'Scipy': 'Scipy',
 'system design': 'system design',
 'Matplotlib': 'Matplotlib',
 'MySQL': 'MySQL',
 'PostgreSQL': 'PostgreSQL',
 'microservice': 'microservice',
 'kubernetes': 'kubernetes',
 'tensorflow serving': 'tensorflow serving',
 'airflow': 'airflow',
 'jenkins': 'jenkins',
 'teamcity': 'teamcity',
 'monitor': 'monitor',
 'shell script': 'shell script',
 'AWS lambda': 'AWS lambda'}

@app.route('/index', methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
	db.drop_all()
	db.create_all()
	if request.method == 'POST':
		# Get the resume and save it into to database.
		if 'resume' not in request.form:
			flash('No input yet')
			return redirect(request.url)
		else:
			resume = request.form['resume']
			resume = User(resume=resume)
			db.session.add(resume)
			db.session.commit()
			
		# Get the job post and save it into database.
		if 'job_description' not in request.form:
			flash('No input yet')
			return redirect(request.url)
		else:
		# Save the submited plain text data into database
			job_post = request.form['job_description']
			job_post = Job(job_post=job_post)
			db.session.add(job_post)
			db.session.commit()
		# Query the database and get the matching score.
		user = User.query.first()
		job = Job.query.first()
		resume=user.resume
		job_post=job.job_post
		matching_score = score.get_score(skills=skills, job_post=job_post, resume=resume)
		classified_title = classify(job_post, preprocessor= tfidfVectorizer, model=classifier)
		return render_template('home.html',matching_score=matching_score, classified_title=classified_title)
	else:
		return render_template('home.html')
		#return 'Saved  to the database!'
		
@app.route('/sendjob', methods=['GET', 'POST'])
def send_job():
	if request.method == 'POST':
		if 'job_post' not in request.form:
			flash('No input yet')
			return redirect(request.url)
		job_post = request.form['job_post']
		job_post = Job(job_post=job_post)
		db.session.add(job_post)
		db.session.commit()
		
		user = User.query.first()
		resume=user.resume
		matching_score = score.get_score(skills=skills, job_post=job_post, resume=resume)
		return render_template('score.html',matching_score=matching_score)
	else:
		return render_template('send_job.html')

if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0", port=5000)
