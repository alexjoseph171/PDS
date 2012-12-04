

import csv
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from collections import Counter
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn import linear_model
import random


datapath = "/Users/mkokkodi/git/PDS/pds_data/"


"""
Remove the csv header, or modify the code.
"""

def createTrainTest():
  rawData = open(datapath+"h5data.csv")
  trainData = open(datapath+ "h5train.csv",'w')
  testData = open(datapath+"h5test.csv",'w')
  for line in rawData:
      if(random.random() > 0.8):
        testData.write(line)
      else:    
        trainData.write(line)
  testData.close()
  trainData.close()     

def getX(line):
  global letterIndex
  tmp = []
  for i in range(0,8):
      if(i==5):
        if line[i] not in lettersDict:
          lettersDict[line[i]] = letterIndex
          letterIndex += 1
      
          
        line[i] = lettersDict[line[i]]
      if i==6 and line[i]=="X":
        line[i]=1
          
      tmp.append(float(line[i]))
  return tmp
        
def loadTrainTest():      
  global number_of_global_ones   

  trainData = csv.reader(open(datapath+"h5train.csv"), delimiter=",")
  for line in trainData:
    train_x.append(getX(line))
    train_y.append(float(line[9]))
  testData = csv.reader(open(datapath+"h5test.csv"), delimiter=",")
  for line in testData:
    test_x.append(getX(line))
    test_y.append(float(line[9]))
    if(line[9]==str(1)):
      number_of_global_ones += 1

def calculateLift(th):
  topX = int(th * (len(problabels)/100))
  i=1
  number_of_ones = 0
  for k in problabels.iterkeys():
    if(test_y[k]==1):
      number_of_ones +=1;
    if i > topX:
      break
    i +=1
  prc_one_top5 = float(number_of_ones)/topX
  prc_one_global = float(number_of_global_ones)/(len(problabels))
  print "Lift "+str(th)+"%:"+ str(prc_one_top5/prc_one_global)
  
def calculateErrorRate(th):
  errors = 0;
  for k,v in problabels.iteritems():
    #print v, test_y[k]

    predictedLabel = 0;    
    if v >= th:
      predictedLabel = 1
      
      
    if(test_y[k]!= predictedLabel):
      errors +=1;
  erroraRate = float(errors)/(len(problabels))
  print "Error rate for threshold "+str(th)+": "+ str(erroraRate)

def getProbabilities(clflogistic):
  
  global problabels
  probabilities =  clflogistic.predict_proba(test_x)
  i = 0
  for line in probabilities:
    problabels[i] = line[1] 
    i += 1
  
  
  problabels = OrderedDict(sorted(problabels.items(), key=lambda x: -x[1]))

def createBalancedTrainingSet():
  ones = 0;
  for label in train_y:
    if label == 1:
      ones += 1
  zeros= len(train_y) - ones
  prc_ones = float(ones)/len(train_y)
  newZeros = 0
  for i in range(0,len(train_y)):
    if(train_y[i] == 0):
      if(random.random() <= prc_ones):
        balanced_train_x.append(train_x[i])
        balanced_train_y.append(train_y[i])
        newZeros +=1
    else:
      balanced_train_x.append(train_x[i])
      balanced_train_y.append(train_y[i])
        
def builtLogistic(train_x,train_y, verbose):    
  clflogistic = LogisticRegression().fit(train_x, train_y)
  getProbabilities(clflogistic)
  if verbose:
    print "------------ Logistic ---------------------"
    errorAnalysis()

def buildTrees(train_x,train_y,verbose):    

  clfTree = tree.DecisionTreeClassifier().fit(train_x, train_y)
  getProbabilities(clfTree)
  if verbose:
    print "------------- Trees ----------------------"
    errorAnalysis()


def errorAnalysis():
  calculateLift(5)
  calculateLift(10)
  calculateLift(20)
  calculateErrorRate(0.5)    

def calculateTpRate():
  x=[]
  for th in range(5,100, 5):
    topX = int(th * (len(problabels)/100))
    i=1
    tp=0
    p=0
    for k,v in problabels.iteritems():
      if(test_y[k]==1):
        p += 1;
        if v >= 0.07: #0.07 is a random threshold. The ranking matters, not the actual threshold.
          tp +=1
      if i > topX:
        break
      i +=1
    #print topX, tp, p 
    x.append(float(tp)/p)
  return x  
  
def buildBayes(train_x,train_y):
  
  gnb = GaussianNB().fit(train_x, train_y)
  getProbabilities(gnb)
  print "------------- Trees ----------------------"
  errorAnalysis()
     
#createTrainTest()
balanced_train_x = []
balanced_train_y= []
train_x = []
train_y = []
test_x = []
test_y = []
lettersDict = {}
letterIndex = 0;

problabels ={} #probs to be 1

number_of_global_ones = 0;


loadTrainTest()
print "-------------------------------------------------------"
print "Question 1:"
print "-------------------------------------------------------"

builtLogistic(train_x, train_y,True)
buildTrees(train_x,train_y,True)

print "-------------------------------------------------------"
print "Question 2"
print "-------------------------------------------------------"

createBalancedTrainingSet()

builtLogistic(balanced_train_x,balanced_train_y,True)
buildTrees(balanced_train_x,balanced_train_y,True)

print "-------------------------------------------------------"
print "Question 3"
print "-------------------------------------------------------"

# Generate data...

buildTrees(train_x,train_y,False)
y = calculateTpRate()
x=[]
for th in range(5,100, 5):
  x.append(th)

plt.scatter(x, y, c='r', s=100,label="Trees")
builtLogistic(train_x, train_y,False)
y = calculateTpRate()
plt.scatter(x, y, c='g', s=50, label= "Logistic")
plt.xlabel("% targeted") # set the x axis label 
plt.ylabel("TPR") # set the y axis label 
plt.legend() # place a legend on the current axes

plt.show()


print "-------------------------------------------------------"
print "Question 4 Naive Bayes"
print "-------------------------------------------------------"
buildBayes(train_x, train_y)

