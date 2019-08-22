import os
import sys
import click
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import get_text

app = Flask(__name__)

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	location = db.Column(db.String(100))
	resume = db.Column(db.LargeBinary)


class Job(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(60))
	#location = db.Column(db.String(100))
	post_date = db.Column(db.String(50))
	job_post = db.Column(db.String(500))
	link = db.Column(db.String(300))
	employer = db.Column(db.String(100))
	
	
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
"""
	path = '../data/'
	job_posts = get_text.get_jobs(path)
	for job, job_post in zip(jobs, job_posts):
		job['job_post'] = job_post 
		
"""
	
	
@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		resume = User(name=file.filename, resume=file.read())
		db.session.add(resume)
		db.session.commit()
		#return 'Saved ' + file.filename + ' to the database!'
		### return top 10 jobs you need to consider today.
		return render_template('jobs.html')
		# return render_template('uploaded.html')
		
# @app.route('/jobs', methods=['GET', 'POST'])
# def get_jobs():



		# return render_template('jobs.html', jobs=jobs)

if __name__=='__main__':
	app.run(debug=True)