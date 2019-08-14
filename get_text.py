# Functions for extract plain text information from uploaded resumes(.docx file) 
import docx
import os
import PyPDF2
import json

def get_doc_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
	
def get_pdf_text(path):	
	pdfFileObj = open(path, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pdfReader.numPages

	resume = pdfReader.getPage(0)
	resume = resume.extractText()
	return resume
	
def get_jobs(path):
	jobs = []
	for filename in os.listdir(path):
		if filename.endswith('.txt'):
			with open(os.path.join(path, filename)) as f:
				jobs.append(f.read())
	return jobs
	
def read_json(path):
	dict = {}
	try:
		with open(path) as json_file:
			dict = json.load(json_file)
		return dict
	except IOError as e:
		print(e)
		exit(1)
	
	
	
	
	
	
	
	
	
	