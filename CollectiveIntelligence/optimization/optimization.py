from __future__ import absolute_import
import time
import random
import math

people = [('Seymour', 'BOS'), ('Franny', 'DAL'), ('Zooey', 'CAK'), ('Walt', 'MIA'), ('Buddy', 'ORD'), ('Les', 'OMA')]

destination = "LGA"

domain=[(0,8)]*(len(people)*2)

flights={}
#
for line in open('./schedule.txt'):
	origin,dest,depart,arrive,price = line.strip().split(',')
	flights.setdefault((origin, dest), [])
	flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
	x = time.strptime(t, '%H:%M')
	return x[3]*60+x[4]

def printschedule(r):
	for d in range(int(len(r)/2)):
		name=people[d][0]
		origin=people[d][1]
		out=flights[(origin,destination)][int(r[d*2])]
		ret=flights[(destination,origin)][int(r[d*2+1])]
		print("%10s%10s %5s-%5s $%3s %5s-%5s $%3s" % (name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[2]))

def schedulecost(sol):
	totalprice=0
	latestarrival=0
	earliestdep=24*60
	
	for d in range(int(len(sol)/2)):
		origin=people[d][1]
		outbound=flights[(origin,destination)][int(sol[d*2])]
		returnf=flights[(destination,origin)][int(sol[d*2+1])]
		
		totalprice+=outbound[2]
		totalprice+=returnf[2]
		
		if latestarrival<getminutes(outbound[1]): latestarrival=getminutes(outbound[1])
		if earliestdep>getminutes(returnf[0]): earliestdep=getminutes(returnf[0])
	
	totalwait=0
	for d in range(int(len(sol)/2)):
		origin=people[d][1]
		outbound=flights[(origin,destination)][int(sol[d*2])]
		returnf=flights[(destination,origin)][int(sol[d*2+1])]
		totalwait+=latestarrival-getminutes(outbound[1])
		totalwait+=getminutes(returnf[0])-earliestdep
	
	if latestarrival<earliestdep: totalprice+=50
	
	return totalprice+totalwait

def allcombination(domain,costf,limit=1000,verbose=True):
	best=999999999
	bestr=None
	
	def combination(i,best,bestr,c):
		if c>limit-1: return best,bestr,c
		for v in range(domain[i][0],domain[i][1]+1):
			r[i]=v
			if i<(len(domain)-1):
				i+=1
				best,bestr,c=combination(i,best,bestr,c)
				i-=1
			else:
				cost=costf(r)
				if cost<best:
					best=cost
					bestr=r[:]
					print(best)
					print(bestr)
				
				c+=1
				if verbose: print(str(c)+" times")
				if c>limit-1: break
				
		return best,bestr,c
	
	c=0
	r=[0 for i in range(len(domain))]
	for i in range(len(domain)):
		best,bestr,c=combination(i,best,bestr,c)
							
	return bestr

def randomoptimize(domain,costf,gr=1000):
	best=999999999
	bestr=None
	for i in range(gr):
		r=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		
		cost=costf(r)
		
		if cost<best:
			best=cost
			bestr=r
			print(best)
			print(r)
					
	return bestr

def hillclimb(domain,costf):
	sol=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
	
	while 1:
		neighbors=[]
		for j in range(len(domain)):
			if sol[j]>domain[j][0]: neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
			if sol[j]<domain[j][1]: neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
		
		current=costf(sol)
		best=current
		for j in range(len(neighbors)):
			cost=costf(neighbors[j])
			if cost<best:
				best=cost
				sol=neighbors[j]
		
		print(best)
		print(sol)
				
		if best==current:
			break
	
	return sol

def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
	vec=[float(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
	
	while T>0.1:
		i=random.randint(0,len(domain)-1)
		
		dir=random.randint(-step,step)
		
		vecb=vec[:]
		vecb[i]+=dir
		if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
		elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]
		
		ea=costf(vec)
		eb=costf(vecb)
		p=pow(math.e,-abs(eb-ea)/T)
		
		if (eb<ea or random.random()<p):
			vec=vecb
			
			print(eb)
			print(vec)
				
		T=T*cool
	
	return vec

def geneticoptimize(domain,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=100):
	def mutate(vec):
		i=random.randint(0,len(domain)-1)
		if random.random()<0.5 and vec[i]>domain[i][0]:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		elif vec[i]<domain[i][1]:
			return vec[0:i]+[vec[i]+step]+vec[i+1:]
		return vec
	
	def crossover(r1,r2):
		i=random.randint(1,len(domain)-2)
		return r1[0:i]+r2[i:]
	
	pop=[]
	for i in range(popsize):
		vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
	
	topelite=int(elite*popsize)
	
	for i in range(maxiter):
		scores=[(costf(v),v) for v in pop]
		scores.sort()
		ranked=[v for (s,v) in scores]
		
		pop=ranked[0:topelite]
		
		while len(pop)<popsize:
			if random.random()<mutprob:
				c=random.randint(0,topelite)
				pop.append(mutate(ranked[c]))
			else:
				c1=random.randint(0,topelite)
				c2=random.randint(0,topelite)
				pop.append(crossover(ranked[c1],ranked[c2]))
														
		print(scores[0][0])
		print(scores[0][1])
	return scores[0][1]

def optimize(domain,costf,printf):
	s=[None]*5
	print("# all combination")
	s[0]=allcombination(domain,costf,limit=100)
	print("# random optimize")
	s[1]=randomoptimize(domain,costf)
	print("# hill-climb optimize")
	s[2]=hillclimb(domain,costf)
	print("# annealing optimize")
	s[3]=annealingoptimize(domain,costf,cool=0.995,step=2)
	print("# genetic optimize")
	s[4]=geneticoptimize(domain,costf)

	if s[0] is not None :
		print("# all combination")
		print(costf(s[0]))
		printf(s[0])
	if s[1] is not None :
		print("# random optimize")
		print(costf(s[1]))
		printf(s[1])
	if s[2] is not None :
		print("# hill-climb optimize")
		print(costf(s[2]))
		printf(s[2])
	if s[3] is not None :
		print("# annealing optimize")
		print(costf(s[3]))
		printf(s[3])
	if s[4] is not None :
		print("# genetic optimize")
		print(costf(s[4]))
		printf(s[4])

# main
#optimize(domain,schedulecost,printschedule)
