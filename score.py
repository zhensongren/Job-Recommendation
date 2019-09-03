#! python3
########################## Data Science Project - Jobs Recommendation Engine ############################################

############################ Install necessary packages below before excuting this script################################
# install the python-docx for word documents
# pip install python-docx 
# install the PyPDF2 for PDF documents 
# pip install PyPDF2
import os
import docx
import PyPDF2

#import pandas as pd
#import numpy as np
from text_vectorizer import TextVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import get_text
"""
############################ Extract words from data files #################################################################
### Read content from resume in PDF format
path = os.path.join('..', 'data', 'DS training LIGANG BAI.pdf')
bai = get_text.get_pdf_text(path)

### Read content from resume in docx file
resume = get_text.get_doc_text('../data/Zhensong Ren_Resume.docx')

### Read skills key words from crawler results
path_DS = os.path.join('..', 'data', 'skills_data_scientist_processed.json')
path_DA = os.path.join('..', 'data', 'skills_data_analyst_processed.json')
path_DE = os.path.join('..', 'data', 'skills_data_engineer_processed.json')
path_MLE = os.path.join('..', 'data', 'skills_machine_learning_engineer_processed.json')
kw_DS = get_text.read_json(path_DS)
kw_DA = get_text.read_json(path_DA)
kw_DE = get_text.read_json(path_DE)
kw_MLE = get_text.read_json(path_MLE)

### Read all the job description files and read into a document list.
path = '../data/'
jobs = get_text.get_jobs(path)

############################################# Vectorize the documents########################################################
tv = TextVectorizer()
tv.fit(kw_MLE) # fit with job skills key words
resume = tv.transform(resume)
bai = tv.transform(bai) 
job0 = tv.transform(jobs[0]) 

############################### Calculating the cosine simlarity as the matching score#######################################

ZS_score = cosine_similarity(resume, job0)[0][0]
bai_score = cosine_similarity(bai, job0)[0][0]
"""
############################### Define a function for calculating matching score #######################################
# Need the skills key word file for vectorization.
def get_score(skills, job_post, resume):
	tv = TextVectorizer()
	tv.fit(skills) # fit with job skills key words
	resume = tv.transform(resume)
	job = tv.transform(job_post) 
	return cosine_similarity(resume, job)[0][0]

"""
############################### Save the calculated Cosine simlarity to 'score.txt' file ####################################
score = open('../data/score.txt', 'w')
score.write('My resume and MLE job matching score : {} \r\n'.format(ZS_score))
score.write('Bai resume and MLE job matching score : {} \r\n'.format(bai_score))
score.write('\r\n')
score.write('Job post used :\r\n {} \r\n'.format(jobs[0]))
score.close()
"""