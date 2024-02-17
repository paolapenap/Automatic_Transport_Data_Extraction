import numpy as np
from numpy import *
import matplotlib.pyplot as plt 
from pylab import *
from matplotlib import rc, rcParams
rc('text',usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern']})
import matplotlib as mpl
#mpl.rcParams['axes.labelsize']= 21 # tamanho de las letras en el grafico
#mpl.rcParams['legend.fontsize']= 20 # tamanho de las letras en la leyenda
#mpl.rcParams['xtick.major.size']= 8
#mpl.rcParams['xtick.minor.size']= 4
#mpl.rcParams['ytick.major.size']= 8
#mpl.rcParams['ytick.minor.size']= 4
mpl.rcParams['xtick.labelsize']=18 # tamanho los numeros en el eje x 
mpl.rcParams['ytick.labelsize']= 18 # tamanho los numeros en el eje y


import glob

import matplotlib as mpl

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
        v1=row_stack((v1,array([float(e[0]),float(e[1]),float(e[3])])))## Magnetic field, electrical resistance, temperature
    v1=v1[1::]
    colors=plt.cm.jet(np.linspace(0,1,nfiles))
    plt.plot(v1[:,0],v1[:,1],label=v1[0,2], color=colors[i])

    from scipy import odr
    def rho_xx(m,x):
        return m[0] + (2*m[1]/np.pi)*(m[2]/((m[2]**2)+(4*(x-m[3])**2)))

    m0=[1e-5,1e-5,1e-2,1e-3]

    linear = odr.Model(rho_xx)
    mydata = odr.Data(v1[:,0],v1[:,1])                   
    myodr  = odr.ODR(mydata, linear, beta0=m0)         
    myoutput = myodr.run()


    plsq      = myoutput.beta                                 # parameters fited
    plsq_err  = myoutput.sd_beta                              # error parameters fited


#    print plsq, plsq_err



    x1=np.arange(-0.2,0.2,0.001)
    y1=rho_xx(plsq,x1)
#    plt.figure()
#    plt.plot(v1[:,0],v1[:,1], 'k.', label=v1[0,2],)
#    plt.plot(x1,y1)
#plt.show()
    
    m=9.11e-31
    e2=(1.6e-19)**2
    n=9.1e15

    tau=m/(n*e2*plsq[0])    
    tau_ast=(m/(n*e2))*(np.pi*plsq[2]/(2*plsq[1]))
    tau_2ee=m/(plsq[2]*sqrt(e2))
#    print tau, tau_ast, tau_2ee


    if i==0:
        v2=array([v1[0,2], max(v1[:,1]), tau, tau_ast, tau_2ee])
    else:
        v2=row_stack((v2,array([v1[0,2], max(v1[:,1]), tau, tau_ast, tau_2ee])))

#print v2
plt.legend()    
plt.xlabel('B (T)',fontsize=25) 
plt.ylabel(r'R', fontsize=25)
plt.show()


#plt.figure()
plt.subplot(221)
plt.plot(v2[:,0], v2[:,1]*1e3, 'k.')
plt.xlabel('T (K)',fontsize=25) 
plt.ylabel(r'$R_0$ (m$\Omega$)', fontsize=25)

plt.subplot(222)
plt.plot(v2[:,0], (1/v2[:,2])*1e-3, 'k.')
plt.xlabel('T (K)',fontsize=25) 
plt.ylabel(r'$1/\tau$ (10$^3$ s$^{-1}$)', fontsize=25)


plt.subplot(223)
plt.plot(v2[:,0], v2[:,3]*1e6, 'k.')
plt.xlabel('T (K)',fontsize=25) 
plt.ylabel(r'$\tau^{\ast}$ ($\mu$s)', fontsize=25)

plt.subplot(224)
plt.plot(v2[:,0], 1e-9/v2[:,4], 'k.')
plt.xlabel('T (K)',fontsize=25) 
plt.ylabel(r'$1/\tau_{2,ee}$ (ns)', fontsize=25)

plt.subplots_adjust(top=0.95, bottom=0.1, left=0.15, right=0.95, hspace=0.35, wspace=0.35)
plt.show()



