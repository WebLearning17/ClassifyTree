#-*-coding=UTF-8-*-
from math import log
import numpy as np
import operator
#计算香农熵
def calShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel=featVec[-1]
        labelCounts[currentLabel]=labelCounts.get(currentLabel,0)+1
    shannonEnt=0.0

    for key in labelCounts:
        prob=float(labelCounts[key])/float(numEntries)
        shannonEnt-=prob*log(prob,2)
    return shannonEnt


def splitDataSet(dataSet,axis,value):
    Vec1=[]
    for veci in dataSet:
        if veci[axis]==value:
            vec2=veci[:axis]
            vec2.extend(veci[axis+1:])
            Vec1.append(vec2)
    return Vec1

#选取最好的数据划分的方式
def chooseBestFeatureToSplit(dataSet):
    #所有的特征
    numFeatures=len(dataSet[0])-1
    #基础的香农熵
    baseEntropy=calShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1

    for i in range(numFeatures):
        #获取特征i 的值列表
        featList=[example[i] for example in dataSet]
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

#多数表决选择叶子的节点
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        classCount[vote]=classCount.get(vote,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#创建树

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    print("bestFeat:",bestFeat)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}

    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

import matplotlib.pyplot as plt
#使用文本注解绘制树节点

#定义文本框和箭头格式
decisionNode=dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
def createPlotSample():
   fig = plt.figure(1, facecolor='white')
   fig.clf()
   createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
   plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
   plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
   plt.show()

#获取叶子节点的数目
def getNumLeafs(myTree):
    numLeafs=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]

    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

#获取树的高度
def getTreeDepth(myTree):
    maxDepth=0
    firstStr=myTree.keys()[0]
    secondStr=myTree[firstStr]
    for key in secondStr.keys():
        if type(secondStr[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondStr[key])
        else:
            thisDepth=1
        if thisDepth>maxDepth:
            maxDepth=thisDepth
    return  maxDepth


def plotMidText(cntrPt,parentPt,txtString):
    xMid=(parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]

    createPlot.ax1.text(xMid,yMid,txtString)


def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]     #the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(secondDict[key],cntrPt,str(key))        #recursion
        else:   #it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
#if you do get a dictonary you know it's a tree, and the first element will be another dict
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()

#createPlot()

def classify(inputTree,featLabels,testVec):
    classLabel1=None
    firstStr=inputTree.keys()[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)

    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel1=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel1=secondDict[key]
    return  classLabel1


#决策树的存储
#使用pickle 模块存储决策树
def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,"w")
    pickle.dump(inputTree,fw)
    fw.close()
def grabTree(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)












