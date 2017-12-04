#Testing Print Graphs
import matplotlib.pyplot as plt
from pylab import *


def printgraph(givenlabel,querysize,totalsize):
	#Slices ordered and plotted clockwise
	a = givenlabel
	labels = a, 'Other Organizations'
	a = querysize
	b = totalsize - querysize
	sizes = [a,b]
	colors = ['red','gold']
	explode =(0.5,0)
	plt.pie(sizes, explode=explode,labels=labels,colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
	plt.axis('equal')
	fig = plt.figure()
	plt.show()
	return
def printlevelgraph(querysize,slice1,slice2,slice3,slice4,slice5,slice6,slice7,slice8,slice9,slice10,totalsize):
	labels = '1','2','3','4','5','6','7','8','9','10','Other'
	b = totalsize - querysize
	sizes=[slice1,slice2,slice3,slice4,slice5,slice6,slice7,slice8,slice9,slice10, b]
	colors = ['blue','green','red','cyan','magenta','yellow','black','white','crimson','orange','darkorchid']
	explode =(0,0,0,0,0,0,0,0,0,0.5,0)
	plt.pie(sizes,explode=explode,labels=labels,colors=colors,autopct='%1.1f%%',shadow=True,startangle=90)
	plt.axis('equal')
	fig = plt.figure()
	plt.show()
	return


#printgraph("yo",123,1230)
