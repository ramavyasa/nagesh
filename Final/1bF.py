
import re
import os
#import nltk
import math
from random import randint

#from nltk.stem.wordnet import WordNetLemmatizer
#lmtzr = WordNetLemmatizer() 

docTrain=[]
docTest=[]
docHeld_out=[]
data=[]
def preProcess():
	all_files = os.listdir('/home1/e1-246-24/Final/gutenberg')
	for file in all_files:
		sentence = []
		f = open('gutenberg/' + file,encoding='utf-8')
		lines = f.readlines()
		#words = lines.split(' ')		
		for line in lines:
			words = line.split(' ')
			for word in words:
				if word != '\n' and word != '':
					if word[-1] == '.' and word not in ['Mr.','Mrs.'] :
						sentence.append(re.sub(r'[^\w\s]','',word.strip().lower()))
						data.append(' '.join(sentence))
						sentence = []
					else:
						sentence.append(re.sub(r'[^\w\s]','',word.strip().lower()))
				
	


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

def back_off(n,gram,doc):

	dash="-"
	snum=0
	
	for s in doc:
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
		snum+=prex
	avg=snum/18	
	print(avg)

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

preProcess()
for i in range(0,len(data)):
	if(i<0.7*len(data)):
		docTrain.append(data[i])
	elif(i<0.85*len(data)):
		docTest.append(data[i])
	else:
		docHeld_out.append(data[i])
print("done Preprocessing")

#preProcess(docHeld_out,"held_out")
#docTrain=docTrain+docHeld_out


for s in docTrain:
	words=s.split(' ')
	gram_find(1,words,gram1)
	gram_find(2,words,gram2)
	gram_find(3,words,gram3)
	gram_find(4,words,gram4)
Gram=[]
print("done")
Gram=[gram1,gram2,gram3,gram4]

print("Calling backoff")
back_off(4	,Gram,docTest)
sent_gen1(Gram)
