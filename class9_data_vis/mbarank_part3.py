import csv as csv
import numpy as np
import matplotlib
from pylab import *
import matplotlib.ticker as ticker
from matplotlib import pyplot as PLT
from operator import itemgetter, attrgetter

#read in and store csv file in numpy recarray object. 
#allows for easy access of columns and rows
 
data = csv2rec('mba3.csv', skiprows=0, delimiter=',')

#getting sorted data for presalary
presalsort = sorted(data, key=itemgetter(4))
getcount = itemgetter(4)
presalary = map(getcount,presalsort)
#print(presalary)

#getting corresponding schools for sorted presalary column
getnames =itemgetter(1)
presalnames =map(getnames,presalsort)
#print(presalnames)

#getting corresponding rank for schools for sorted presalary
getrank =itemgetter(0)
rankpresal =map(getrank,presalsort)

#mapping names to rankings in order to create a new list with rank + school name
presalranknames = rankpresal
for i, (a, b) in enumerate(zip(presalnames, rankpresal)):
 presalranknames[i] = "%s (%s)" % (a, b)

#sorting average salary
avgsalsort = sorted(data, key=itemgetter(3))
getsalcount = itemgetter(3)
avgsal = map(getsalcount,avgsalsort)

#getting corresponding schools for sorted avgsalary
getsalschoolnames =itemgetter(1)
avgsalschool = map(getsalschoolnames,avgsalsort)
#print(avgsalschool)

#getting corresponding rank for schools for sorted avgsal
getrank_avgsal =itemgetter(0)
rankavgsal =map(getrank_avgsal,avgsalsort)
#print(rankavgsal)

#mapping names to rankings in order to create a new list with rank + school name
avgsalranknames = rankavgsal
for i, (a, b) in enumerate(zip(avgsalschool, rankavgsal)):
  avgsalranknames[i] = "%s (%s)" % (a, b)

#sorting % of grads with jobs
gradjobssort = sorted(data, key=itemgetter(5))
#getting sorted data for column 5 GradJobs
getgradjobs = itemgetter(5)
gradjobs = map(getgradjobs,gradjobssort)
#print(gradjobs)

#getting corresponding schools for sorted column 3 data
getgradjobschoolnames =itemgetter(1)
gradjobsschool = map(getgradjobschoolnames,gradjobssort)
#print(gradjobsschool)

#getting corresponding rank for schools for sorted column
getrank_jobs =itemgetter(0)
rankjobs =map(getrank_jobs,gradjobssort)
#print(rankjobs)

#mapping names to rankings in order to create a new list with rank + school name
rankjobnames = rankjobs
for i, (a, b) in enumerate(zip(gradjobsschool, rankjobs)):
  rankjobnames[i] = "%s (%s)" % (a, b)

#getting sorted data for PhD
phdsort = sorted(data, key=itemgetter(6))
phdcount = itemgetter(6)
phdlist = map(phdcount, phdsort)
#print(phdlist)

#getting corresponding schools for sorted PhD data
getphdschoolnames =itemgetter(1)
phdnames = map(getphdschoolnames,phdsort)
#print(phdnames)

#getting corresponding rank for schools for sorted column
getphd_rank =itemgetter(0)
phdrank =map(getphd_rank, phdsort)
#print(phdrank)
 
#Create a figure canvas for plotting multiple graphs

fig = PLT.figure(linewidth=0.0,frameon=True, dpi=80, figsize=(17,8))
fig.canvas.set_window_title('MBA Rankings')
fig.patch.set_facecolor('#FFFFFF')
matplotlib.rc('xtick', labelsize=9, color='#000000') # setting font size for x & y
matplotlib.rc('ytick', labelsize=9, color='#000000') 

#barchart horizontal %presalary

ax1 = fig.add_subplot(131, frameon=False, axis_bgcolor='#FFFFFF')

#remove all those annoying ticks
for a in ax1.yaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

for a in ax1.xaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

val = presalary    # the bar lengths
pos = arange(len(presalary)) +.5    # the bar centers on the y axis
rects = ax1.barh(pos,val, align='center', edgecolor='#CCCCCC', height=.25, color='#CCCCCC')
yticks(pos, (presalranknames))
xlabel('Pre Salary %')

#Plot a solid vertical gridline to highlight the avg position
plt.plot([76,76], [0, 26], 'r', alpha=0.25, lw=2)

#barchart horizontal avgsalary - working
ax2 = fig.add_subplot(132, frameon=False, axis_bgcolor='#FFFFFF')

#remove all those annoying ticks

for a in ax2.yaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

for a in ax2.xaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

val1 = avgsal    # the bar lengths
pos1 = arange(len(data)) +.5    # the bar centers on the y axis
rects = ax2.barh(pos1,val1, edgecolor='#CCCCCC', align='center', height=.25, color='#CCCCCC')

"""
dividing the x axis by 1000. creating a function called convertx. Then calling it below.

"""
def convertx (x,pos=None):
    return "%d" % (x/1000)

ax2.xaxis.set_major_formatter(ticker.FuncFormatter(convertx))
ax2.set_xlabel('Average Salary in USD(000s)')

#the y axis will include school + rank by referring to the avgsalranknames list
yticks(pos1, (avgsalranknames))
xlabel('Average Salary')

#Plot a solid vertical gridline to highlight the avg position. Hardcoded value for illustration purposes. 
plt.plot([113732,113732], [0, 26], 'r', alpha=0.25, lw=2)

##barchart horizontal gradjobs
ax3 = fig.add_subplot(133, frameon=False, axis_bgcolor='#FFFFFF')

#remove all those annoying ticks

for a in ax3.yaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

for a in ax3.xaxis.majorTicks:
  a.tick1On=False
  a.tick2On=False

val2 = gradjobs    # the bar lengths
pos2 = arange(len(data)) +.5    # the bar centers on the y axis

rects = ax3.barh(pos2,val2, align='center', edgecolor='#CCCCCC', height=.25, color='#CCCCCC')
yticks(pos2, (rankjobnames))
xlabel('% Graduates with Jobs')

#Plot a solid vertical gridline to highlight the avg position. Hardcoded value for illustration purposes. 
plt.plot([93,93], [0, 26], 'r', alpha=0.25, lw=2)

PLT.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
PLT.show()
