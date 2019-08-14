import numpy as np
class TextVectorizer(object):

	def fit(self, kw):
		self.word_idx = {}
		self.kw = kw # a dict of skills key words
		# Encode the keywords as integers
		for i, word in enumerate(kw.keys()):
			self.word_idx[word] = i
		
	def transform(self, doc):
		# Initialize the vector array as [0,0,0...,0]
		doc_vec = np.zeros(len(self.word_idx))
		for k, v in self.kw.items():
			if k in set(doc.split()):
				doc_vec[self.word_idx[k]] = 1
		doc_vec = np.array(doc_vec).reshape(1,-1)
		return doc_vec

	def fit_transform(self, X, y=None):
		self.fit(X)
		return self.transform(X)