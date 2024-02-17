import numpy as np
from numpy import *
import matplotlib.pyplot as plt 
from pylab import *
from matplotlib import rc, rcParams
rc('text',usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern']})
mpl.rcParams['xtick.labelsize']= 18 # tamanho los numeros en el eje x
mpl.rcParams['ytick.labelsize']= 18 # tamanho los numeros en el eje y


import glob

filenames = sorted(glob.glob('1416-36_I5-11V1-7R100kVosc1VT1K_5_*.dat'))
filenames = filenames[0::]

nfiles = len(filenames)
#print(nfiles)

for i,f in enumerate(filenames):
    #print(f)
    data = open(f,'r').readlines()
    v1=zeros((3))
    for e in data[1::]:
        e=e.split('	')
        v1=row_stack((v1,array([float(e[0]),float(e[1]),float(e[3])])))
    v1=v1[1::]
    colors=plt.cm.jet(np.linspace(0,1,nfiles))
    plt.plot(v1[:,0],v1[:,1]*1e6,label=v1[0,2], color=colors[i])


plt.legend()    
plt.xlabel('B (T)',fontsize=25) 
plt.ylabel(r'R ($\mu\Omega$)', fontsize=25)
plt.show()
