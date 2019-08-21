import os
import sys
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
db = SQLAlchemy(app)

class FileContents(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)
	
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
		newfile = FileContents(name=file.filename, data=file.read())
		db.session.add(newfile)
		db.session.commit()
		return 'Saved ' + file.filename + ' to the database!'

if __name__=='__main__':
	app.run(debug=True)