import numpy as np
from numpy import *
import matplotlib.pyplot as plt 
from pylab import *
from matplotlib import rc, rcParams
import matplotlib as mpl
rc('text',usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern']})


import glob

import os



filenames1 = glob.glob('1416-36_I5-7V1-2R100kVosc1VT1K_29_*.dat')
filenames1 = sorted(filenames1, key=os.path.getmtime)

filenames1 = filenames1[0::]

for i,f in enumerate(filenames1):
    data = open(f,'r').readlines()
    v1=zeros((3))
    for e in data[1::]:
        e=e.split('	')
        v1=row_stack((v1,array([float(e[0]),float(e[1]),float(e[3])])))## Magnetic field, electrical resistance, temperature
    v1=v1[1::]

    if i==0:
        v2=array([v1[0,2], max(v1[:,1])])
    else:
        v2=row_stack((v2,array([v1[0,2], max(v1[:,1])])))###Temperature, Zero-field-resistance





filenames2 = glob.glob('1416-13_I1-2V7-8R100kVosc1Vfosc11HzTsweep_23_*.dat')
filenames2 = sorted(filenames2, key=os.path.getmtime)

filenames2 = filenames2[0::]

for i,f in enumerate(filenames2):
    data = open(f,'r').readlines()
    v3=zeros((3))
    for e in data[1::]:
        e=e.split('	')
        v3=row_stack((v3,array([float(e[0]),float(e[1]),float(e[3])])))## Magnetic field, electrical resistance, temperature
    v3=v3[1::]
   
    if i==0:
        v4=array([v3[0,2], max(v3[:,1])])
    else:
        v4=row_stack((v4,array([v3[0,2], max(v3[:,1])])))###Temperature, Zero-field-resistance



T_Am36 = v2[:,0]
R_Am36 = v2[:,1]*1e5


T_Am13 = v4[:,0]
R_Am13 = v4[:,1]*1e5

from scipy import interpolate
from scipy.interpolate import interp1d

T_Am36_or=T_Am36.argsort() 
T_Am36=take(T_Am36,T_Am36_or) 
R_Am36=take(R_Am36,T_Am36_or)


T_Am13_or=T_Am13.argsort() 
T_Am13=take(T_Am13,T_Am13_or) 
R_Am13=take(R_Am13,T_Am13_or)



s36= interp1d(T_Am36, R_Am36, kind='slinear') 
s13= interp1d(T_Am13, R_Am13, kind='slinear')


ming2=min(T_Am36) 
if min(T_Am36)<min(T_Am13) : ming2=min(T_Am13) 


maxg2=max(T_Am36) 
if max(T_Am36) < max(T_Am13) : maxg2=max(T_Am36)


xnew2 = np.linspace(ming2,maxg2,30) 
ynew36 = s36(xnew2)
ynew13 = s13(xnew2) 



Diff_R= ynew36 - ynew13

VDiff=np.column_stack((xnew2, ynew36, ynew13, Diff_R))
np.savetxt('Diff_RAm36-RAm13_vs_T', VDiff , delimiter=' ', fmt='%1.6e')

plt.subplot(111)
plt.plot(T_Am36, R_Am36, 'bo', label='Holes')
plt.plot(xnew2, ynew36, 'b')
plt.plot(T_Am13, R_Am13, 'g^', label='No-Holes')
plt.plot(xnew2, ynew13, 'g')
plt.plot(xnew2, Diff_R, 'rs', label='Diff')
plt.xlabel('T (K)',fontsize=25) 
plt.ylabel(r'R ($\Omega$)', fontsize=25)
plt.legend()
plt.subplots_adjust(top=0.9, bottom=0.15, left=0.15, right=0.95)
plt.show()
