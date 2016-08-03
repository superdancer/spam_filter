# -*- coding: utf-8 -*-
import sys
import random
import re
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
def getNmlContent(filePath):
    f=open(filePath,'r')
    lines=f.readlines()
    content=set([])
    flag=False
    for line in lines:
        if 'X-UIDL:' in line:
            flag=True
            continue
        if  (not 'X-UIDL:' in line) and (not flag):
            continue
        if 'Re:' in line:
            break
        else:
            if line!='\n' and line!=': \n':
                try:
                    line = line.decode('utf-8')
                except Exception,e:
                    line = line.decode('GBK')
                str=''
                for i in range(len(line)):
                    if is_chinese(line[i]):
                        str+=line[i]
                lineList=jieba.cut(str)
                lineList=list(lineList)
                content=content|set(lineList)
                content=content-stopwords
    #print '/'.join(content)
    return list(content)
def getSpamContent(filePath):
    f=open(filePath,'r')
    lines=f.readlines()
    content=set([])
    for line in lines:
        try:
            line = line.decode('utf-8')
        except Exception,e:
            line = line.decode('GBK')
        str=''
        for i in range(len(line)):
            if is_chinese(line[i]):
                str+=line[i]
        if str:
            lineList=jieba.cut(str)
            lineList=list(lineList)
            content=content|set(lineList)
            content=content-stopwords
    #print '/'.join(content)
    return list(content) 
def getStopWords(filePath):
    f=open(filePath,'r')
    lines=f.readlines()
    content=set([])
    for line in lines:
        try:
            line = line.decode('utf-8').encode('gbk','ignore').decode('gbk')
        except Exception,e:
            line = line.decode('GBK')  
        content.add(line.strip())
    #print '/'.join(content)
    return content   
def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False
dataNoNml=[]
dataNoSpm=[]
def loadDataSet(num):
    
#if __name__=='__main__':
    dataSet=[]
    label=[]
    
    countNml=0
    countSpm=0
    
    global dataNoNml
    global dataNoSpm
    
    #加载停用词
    global stopwords
    f='D:\\code\\spam_filter\\data\\stopwords.txt'
    stopwords=getStopWords(f)
    
    #加载正常邮件
    while countNml<num/2:
        m=random.randint(1,8001)
        if not m in dataNoNml:
            f='D:\\code\\spam_filter\\data\\normal\\{0}.txt'.format(m)
            try:
                data=getNmlContent(f)
            except IOError,e:
                print e
            else:
                dataSet.append(data)
                label.append(0)
                dataNoNml.append(m)
                countNml+=1
    
    #加载垃圾邮件
    while countSpm<num/2:
        m=random.randint(1,8001)
        if not m in dataNoSpm:
            f='D:\\code\\spam_filter\\data\\spam\\{0}.txt'.format(m)
            try:
                data=getSpamContent(f)
            except IOError,e:
                print e
            else:
                dataSet.append(data)
                label.append(1)
                dataNoSpm.append(m)
                countSpm+=1
    return dataSet,label
    
def getTestData(n):
    global dataNoNml
    global dataNoSpm
    dataSet,label= loadDataSet(n)
    #dataNoNml=[]
    #dataNoSpm=[]
    return dataSet,label