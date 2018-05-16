#-*-coding=UTF-8-*-
#使用决策树绘制 图形

from trees import *


dataSet=[
    [1,1,'yes'],
    [1,1,'yes'],
    [1,0,'no'],
    [0,1,'no'],
    [0,1,'no']

]
labels=['no surfacing','flippers']

myTree=createTree(dataSet,labels)
print(myTree)
createPlot(myTree)
