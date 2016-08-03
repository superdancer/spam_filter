#-*- coding: UTF-8 -*-
from numpy import *
import sys
from getContent import *
reload(sys)
sys.setdefaultencoding("utf-8")


def createWordsVector(dataSet):
    global wordsVector
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    wordsVector=list(vocabSet)

def setWords2Vec(words):
    returnVec=[0]*len(wordsVector)
    for word in words:
        if word in wordsVector:
            returnVec[wordsVector.index(word)]=1
    return returnVec
    
def trainNB0(trainMatrix,trainCategory):
    global wordsProbNormal
    global wordsProbSpam
    global probSpam
    numRowDocs=len(trainMatrix)#文档数
    numColWords=len(trainMatrix[0])#词向量数
    probSpam=sum(trainCategory)/float(numRowDocs)#某个类别的概率
    wordsNumInAbusiveDocs=ones(numColWords)
    wordsNumInNormalDocs=ones(numColWords)
    sumInAbusive=2.0
    sumInNormal=2.0
    
    for i in range(numRowDocs):
        if trainCategory[i]==1:
            wordsNumInAbusiveDocs+=trainMatrix[i]
            sumInAbusive+=sum(trainMatrix[i])
        else:
            wordsNumInNormalDocs+=trainMatrix[i]
            sumInNormal+=sum(trainMatrix[i])
    wordsProbSpam=log(wordsNumInAbusiveDocs/sumInAbusive)#每个词在侮辱性的文档中出现的概率
    wordsProbNormal=log(wordsNumInNormalDocs/sumInNormal)#每个词在正常文档中出现的概率

def classify(testVec):
    global wordsProbNormal
    global wordsProbSpam
    testVec=setWords2Vec(testVec)
    testVec=array(testVec)
    wordsProbNormal=array(wordsProbNormal)
    wordsProbSpam=array(wordsProbSpam)

    p0=sum(testVec*wordsProbNormal)+log(1-probSpam)
    p1=sum(testVec*wordsProbSpam)+log(probSpam)
    
    print p0,p1
    if p0>p1:
        print u'正常'
        return 0
    elif p0<p1:
        print u'------->垃圾'
        return 1
    else:
        print u'---------------------->不确定'
        return 0
def train(trainSet,label):

    createWordsVector(trainSet)
    trainMat=[]
    for data in trainSet:
        vec=setWords2Vec(data)
        trainMat.append(vec)  
    trainNB0(trainMat,label) 
    
    
if __name__=='__main__':
    trainNum=1000
    testNum=100
    testSet,testLabel=getTestData(testNum)#获取测试集
    trainSet,trainLabel=loadDataSet(trainNum)#获取训练集

    train(trainSet,trainLabel)           #模型训练
    
    print testLabel

    wrongN=[]
    wrongS=[]
    correct=0.0
    for i in range(testNum):
        result=classify(testSet[i])
        if result == testLabel[i]:
            correct+=1
        else:
            if i<testNum/2:
                wrongN.append(i)
            else:
                wrongS.append(i-testNum/2)
    
    for i in range(len(wrongN)):
        print 'normal ',dataNoNml[wrongN[i]]
    for i in range(len(wrongS)):
        print 'spam ',dataNoSpm[wrongS[i]]
    print correct
    print 'correct rate: ',correct/(testNum)

    