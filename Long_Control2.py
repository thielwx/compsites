#!/usr/bin/env python
# coding: utf-8



#This script is the insane attempt to run entire days separately and then put them together 
#into weekly/monthly/seasonal composites

#The script will run on a day by day basis, and be made so that each command has an assocaited function.
#So if I already have the data I will be able to only run certain parts



import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import datetime
import pandas as pd
import subprocess as sp

import sys


#==========================================================
# Function land
#==========================================================

# # 2) Run glmtools



def glmtools(case,start_date,end_date):

    cmd = 'python /localdata/PyScripts/utilities/runglmtools-fast.py '+case+' '+start_date+'0000 '+end_date+'0000'
    p = sp.Popen(cmd,shell=True)
    p.wait()

    return 0


def glmremove(case,start_date,end_date):
    cmd = 'rm -rf /localdata/cases/'+case+'/GLM/'
    p = sp.Popen(cmd,shell=True)
    p.wait()

    return 0




#============================================================
# Run like this: python Long_Control2.py 'casename' YYYY/MM/DD(start) YYYY/MM/DD(end)
#===========================================================


startDT = datetime.datetime.now()

args = sys.argv

case = args[1]
start_date = args[2]
end_date = args[3]




#Getting list of dates to pull from
datetime_list = pd.date_range(start=start_date,end=end_date,freq='D').to_pydatetime().tolist()

#Converting this into a list of dates that we can use later in the functions
start_list = []
end_list = []
timedelta = datetime.timedelta(days=1)

#For loop to create the start and end lists
for i in datetime_list:
    
    timestr = i.strftime('%Y%m%d')
    start_list.append(timestr)
    
    endtime = i + timedelta
    endstr = endtime.strftime('%Y%m%d')
    end_list.append(endstr)
    
indexes = np.arange(0,len(start_list))





for i in indexes:
    glmtools(case+'/'+start_list[i],start_list[i],end_list[i])
    glmremove(case+'/'+start_list[i],start_list[i],end_list[i])


endDT = datetime.datetime.now()
totalDT = endDT-startDT

print ('Start time: '+str(startDT))
print ('End time:   '+str(endDT))
print ('Total running time: '+str(totalDT))
    
    




