import re
import math

def getwords(doc):
	splitter=re.compile('\\W*')
	words=[s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
	return dict([(w,1) for w in words])

class classifier:
	def __init__(self,getfeatures,filename=None):
		self.fc={}
		self.cc={}
		self.getfeatures=getfeatures
	
	def incf(self,f,cat):
		self.fc.setdefault(f,{})
		self.fc[f].setdefault(cat,0)
		self.fc[f][cat]+=1
	
	def incc(self,cat):
		self.cc.setdefault(cat,0)
		self.cc[cat]+=1
	
	def fcount(self,f,cat):
		if f in self.fc and cat in self.fc[f]:
			return float(self.fc[f][cat])
		return 0.0
	
	def catcount(self,cat):
		if cat in self.cc:
			return float(self.cc[cat])
		return 0
	
	def totalcount(self):
		return sum(self.cc.values())
	
	def categories(self):
		return self.cc.keys()
	
	def train(self,item,cat):
		features=self.getfeatures(item)
		for f in features:
			self.incf(f,cat)
		self.incc(cat)
	
	def fprob(self,f,cat):
		if self.catcount(cat)==0: return 0
		return self.fcount(f,cat)/self.catcount(cat)
	
	def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
		basicprob=prf(f,cat)
		totals=sum([self.fcount(f,c) for c in self.categories()])
		return ((weight*ap)+(totals*basicprob))/(weight+totals)

def sampletrain(cl):
	cl.train('the quick brown fox jumps over the lazy dog','good')
	cl.train('make quick money in the online casino','bad')
	cl.train('Nobody owns the water.','good')
	cl.train('the quick rabbit jumps fences','good')
	cl.train('buy pharmaceuticals now','bad')

class naivebayes(classifier):
	def __init__(self,getfeatures):
		classifier.__init__(self,getfeatures)
		self.thresholds={}
	
	def docprob(self,item,cat):
		features=self.getfeatures(item)
		p=1
		for f in features: p*=self.weightedprob(f,cat,self.fprob)
		return p
	
	def prob(self,item,cat):
		catprob=self.catcount(cat)/self.totalcount()
		docprob=self.docprob(item,cat)
		return docprob*catprob
	
	def setthreshold(self,cat,t):
		self.thresholds[cat]=t
	
	def getthreshold(self,cat):
		if cat not in self.thresholds: return 1.0
		return self.thresholds[cat]
	
	def classify(self,item,default=None):
		probs={}
		max=0.0
		for cat in self.categories():
			probs[cat]=self.prob(item,cat)
			if probs[cat]>max:
				max=probs[cat]
				best=cat
		
		for cat in probs:
			if cat==best: continue
			if probs[cat]*self.getthreshold(best)>probs[best]: return default
		return best

class fisherclassifier(classifier):
	def __init__(self,getfeatures):
		classifier.__init__(self,getfeatures)
		self.minimums={}
		
	def cprob(self,f,cat):
		clf=self.fprob(f,cat)
		if clf==0: return 0
		
		freqsum=sum([self.fprob(f,c) for c in self.categories()])
		p=clf/(freqsum)
		return p

	def fisherprob(self,item,cat):
		p=1
		features=self.getfeatures(item)
		for f in features:
			p*=(self.weightedprob(f,cat,self.cprob))
		fscore=-2*math.log(p)
		return self.invchi2(fscore,len(features)*2)
	
	def invchi2(self,chi,df):
		m=chi/2.0
		sum=term=math.exp(-m)
		for i in range(1,df//2):
			term*=m/i
			sum+=term
		return min(sum,1.0)
	
	def setminimum(self,cat,min):
		self.minimums[cat]=min
	
	def getminimum(self,cat):
		if cat not in self.minimums: return 0
		return self.minimums[cat]
	
	def classify(self,item,default=None):
		best=default
		max=0.0
		for c in self.categories():
			p=self.fisherprob(item,c)
			if p>self.getminimum(c) and p>max:
				best=c
				max=p
		return best
	
cl=classifier(getwords)
sampletrain(cl)
print(cl.weightedprob('money','good',cl.fprob))
sampletrain(cl)
print(cl.weightedprob('money','good',cl.fprob))

cl=naivebayes(getwords)
sampletrain(cl)
print(cl.prob('quick rabbit','good'))
print(cl.prob('quick rabbit','bad'))

cl=naivebayes(getwords)
sampletrain(cl)
print(cl.classify('quick rabbit',default='unknown'))
print(cl.classify('quick money',default='unknown'))
cl.setthreshold('bad',3.0)
print(cl.classify('quick money',default='unknown'))
for i in range(10): sampletrain(cl)
print(cl.classify('quick money',default='unknown'))

cl=fisherclassifier(getwords)
sampletrain(cl)
print(cl.cprob('quick','good'))
print(cl.cprob('money','bad'))
print(cl.weightedprob('money','bad',cl.cprob))

print(cl.fisherprob('quick rabbit','good'))
print(cl.fisherprob('quick rabbit','bad'))

print(cl.classify('quick rabbit'))
print(cl.classify('quick money'))
cl.setminimum('bad',0.8)
print(cl.classify('quick money'))
cl.setminimum('good',0.4)
print(cl.classify('quick money'))
