from random import random, randint
import math

def wineprice(rating,age):
	peak_age=rating-50
	
	price=rating/2
	if age>peak_age:
		price=price*(5-(age-peak_age))
	else:
		price=price*(5*((age+1)/peak_age))
	if price<0: price=0
	return price

def wineset1():
	rows=[]
	for i in range(300):
		rating=random()*50+50
		age=random()*50
		price=wineprice(rating,age)
		price*=(random()*0.4+0.8)
		rows.append({'input':(rating,age),'result':price})
	return rows

def euclidean(v1,v2):
	d=0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return math.sqrt(d)

def getdistances(data,vec1):
	distancelist=[]
	for i in range(len(data)):
		vec2=data[i]['input']
		distancelist.append((euclidean(vec1,vec2),i))
	distancelist.sort()
	return distancelist

def knnestimate(data,vec1,k=5):
	dlist=getdistances(data,vec1)
	avg=0.0
	for i in range(k):
		idx=dlist[i][1]
		avg+=data[idx]['result']
	avg=avg/k
	return avg

def inverseweight(dist,num=1.0,const=0.1):
	return num/(dist+const)

def subtractweight(dist,const=1.0):
	if dist>const:
		return 0
	else:
		return const-dist

def gaussian(dist,sigma=10.0):
	return math.e**(-dist**2/(2*sigma**2))

def weighedknn(data,vec1,k=5,weightf=gaussian):
	dlist=getdistances(data,vec1)
	avg=0.0
	totalweight=0.0
	for i in range(k):
		dist=dlist[i][0]
		idx=dlist[i][1]
		weight=weightf(dist)
		avg+=weight*data[idx]['result']
		totalweight+=weight
	avg=avg/totalweight
	return avg

def dividedata(data,test=0.05):
	trainset=[]
	testset=[]
	for row in data:
		if random()<test:
			testset.append(row)
		else:
			trainset.append(row)
	return trainset,testset

def testalgorithm(algf,trainset,testset):
	error=0.0
	for row in testset:
		guess=algf(trainset,row['input'])
		error+=(row['result']-guess)**2
	return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.05):
	error=0.0
	for i in range(trials):
		trainset,testset=dividedata(data,test)
		error+=testalgorithm(algf,trainset,testset)
	return error/trials

print('Actual data')
print(wineprice(95.0,3.0))
print(wineprice(99.0,3.0))
print(wineprice(99.0,5.0))

data=wineset1()
print('KNN K=5')
print(knnestimate(data,(95.0,3.0)))
print(knnestimate(data,(99.0,3.0)))
print(knnestimate(data,(99.0,5.0)))

print('KNN K=1')
print(knnestimate(data,(95.0,3.0),k=1))
print(knnestimate(data,(99.0,3.0),k=1))
print(knnestimate(data,(99.0,5.0),k=1))

print('WKNN K=5')
print(weighedknn(data,(95.0,3.0)))
print(weighedknn(data,(99.0,3.0)))
print(weighedknn(data,(99.0,5.0)))


def knn3(d,v): return knnestimate(d,v,k=3)
def knn1(d,v): return knnestimate(d,v,k=1)
def knninverse(d,v): return weighedknn(d,v,weightf=inverseweight)
print(crossvalidate(knnestimate,data))
print(crossvalidate(knn3,data))
print(crossvalidate(knn1,data))
print(crossvalidate(knninverse,data))
