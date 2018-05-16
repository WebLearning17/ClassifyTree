#-*-coding=UTF-8-*-
#使用决策树进行分类
from trees import  *
dataSet=[
    [1,1,'yes'],
    [1,1,'yes'],
    [1,0,'no'],
    [0,1,'no'],
    [0,1,'no']

]
labels=['no surfacing','flippers']
myTree=createTree(dataSet,labels[:])
storeTree(myTree,"myTree.model")
print (myTree)
result=classify(myTree,labels,[1,1])
print(result)
