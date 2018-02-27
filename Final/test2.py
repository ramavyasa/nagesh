#!/usr/bin/python3
import re
import sys
#import nltk
import os
import math
import numpy as np
from random import *
#from nltk.stem.wordnet import WordNetLemmatizer
#lmtzr = WordNetLemmatizer()


docTrain=list()
docTest =list()
add_all=set()

def preProcess(doc,filename):

	all_files = open(filename)

	for file in all_files:
		f = open("brown/"+file.strip())
			
		sentances=list()

		for i in f.readlines():
			if(i=='\n'):
				continue;

			sent=""
			sep=i.split(' ') 
			for j in sep:
				k=j.split('/')

				j=re.sub(r'[^\w\s*]','',re.sub(r'/.*','',j.lower().strip()))
				if(len(k)>1):
					if(j!="" and len(k[1])>0):
						pos = 'v' if (k[1][0] == 'v' or k[1][0] == 'b') else 'n'
						#j= lmtzr.lemmatize(j,pos)
						add_all.add(j)
						sent=sent+j+" "		
			sentances.append(sent)

		doc.append(sentances)	
	#for sent in sentances:
			#print(sent)
gram1=dict()		
gram2=dict()
gram3=dict()
gram4=dict()
def gram_find(n,words,gram):

	wordc=""
	dash="-"
	for i in range(len(words)):
		if(i>=n):
			wordc=dash.join(words[i-n:i])
			if(wordc in gram):
				gram[wordc]+=1
			else:
				gram[wordc]=1

def back_off(n,gram,doc):

	dash="-"
	sum_=0
	for d in doc:
		for s in d:
			if(len(s)==0):
				continue
			prob=0
			words=s.split(' ')
			
			for i in range(n,len(words)):
				
				k=n
				while True:
					wordc=dash.join(words[i-k:i])
					prev=dash.join(words[i-k:i-1])
					if(wordc not in gram[k-1] and k>1):
						k-=1
					else:
						break;
	
				if(k==1):
					prob += math.log(gram[0][i]/sum(gram[0].values())) if i in gram[0] else 1/len(gram[0])
				else:
					prob += math.log(gram[k-1][wordc]/gram[k-2][prev])

			prex=math.exp(prob*-1/len(s)) if len(s)!=0 else 0
			sum_+=prex
	print(sum_/len(doc))		



def test(n,gram,gramPrev,v):
	wordc=""
	dash="-"
	perplex=0
	
	for d in docTest:
		for s in d:
			prob=1
			words = s.split(' ')
			for i in range(n,len(words)):
				wordc=dash.join(words[i-n:i])
				prev =dash.join(words[i-n:i-1])
				if(wordc in gram):
					w2=gram[wordc]
					w1=gramPrev[prev]  
				else:
					w2=0
					w1=0
					if(prev in gramPrev):
						w1=gramPrev[prev]

				prob +=math.log((w2+1)/(w1+v))

			perplex +=np.exp(-1/n*prob) 	
			 		
	doc_avg=perplex/len(docTest)	
	print(doc_avg)

def sent_gen1(gram):
	sent=""
	wd_1 =list(gram[3])
	val_1=list(gram[3].values())	
	sort_1=sorted(enumerate(val_1), key=lambda x: x[1],reverse=True)
	r =randint(0,10)
	wordc = wd_1[sort_1[r][0]]
	sent=wordc
	for i in range(1,7):

		beg=0
		wd_2=[]
		val_2=[]
		b=False

		for k in range(3,0,-1):	
			beg =wordc.index("-",beg+1)
			prev_w =wordc[ beg + 1: ]
			
			for w in gram[0]:
				next_w = prev_w+"-"+w
				
				if next_w in gram[k]:
					b=True
					wd_2.append(w)
					val_2.append(gram[k][next_w])
			if(b):
				break		
		if(b):
			r =randint(0,len(wd_2)-1)
			sort_2=sorted(enumerate(val_2), key=lambda x: x[1],reverse=True)
			new_word = wd_2[sort_2[r][0]]
		else:
			print("true")
			r=randint(0,10)
			new_word=wd_1[sort_1[r][0]]
		sent+="-"+new_word
		wordc=wordc[wordc.index("-")+1:]+"-"+new_word
	print(sent)			
				

def sent_gen2(gram):
	sent=""
	wd_1 =list(gram[0])
	val_1=list(gram[0].values())	
	sort_1=sorted(enumerate(val_1), key=lambda x: x[1],reverse=True)
	r =randint(0,10)
	wordc = wd_1[sort_1[r][0]]

	for i in range(1,10):
		val_2=[]
		wd_2 =[]
		b = True
		sent=sent+wordc+" "
		pattern = re.compile(wordc+"-.*")
		for w in gram[1]:
			if(pattern.match(w)):		
				b = False
				wd_2.append(w)
				val_2.append(gram[1][w])
		sort_2=sorted(enumerate(val_2), key=lambda x: x[1],reverse=True)
		if(b):
			r =randint(0,100)
			wordc = wd_1[sort_1[r][0]]
		else:	
			r =randint(0,len(wd_2))
			wordc = wd_2[sort_2[r][0]].split('-')[1]
			print(wordc)
			
	print(sent)			


docHeld_out=[]
preProcess(docTrain,"train")
print("done Preprocessing")

V=len(add_all)
print("done Testing")
preProcess(docTest,"test")

preProcess(docHeld_out,"held_out")
docTrain=docTrain+docHeld_out

for d in docTrain:
	for s in d:
		words=s.split(' ')
		gram_find(1,words,gram1)
		gram_find(2,words,gram2)
		gram_find(3,words,gram3)
		gram_find(4,words,gram4)
Gram=[]
print("done")
Gram=[gram1,gram2,gram3,gram4]

print("Calling backoff")
back_off(4,Gram,docTest)
sent_gen1(Gram)


