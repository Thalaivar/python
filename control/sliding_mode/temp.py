import matplotlib.pyplot as plt
from scipy.integrate import ode
import numpy as np
from numpy import sin,cos,tan,zeros,exp,tanh,dot,array
from scipy.interpolate import interp1d
from matplotlib import rc

def f(t,Y,param):
    x1,x2=Y[0],Y[1]
    eta,k,lam=param[0],param[1],param[2]
    e=x1-1
    de=x2
    s=de+lam*e
    m,c=3+1.5*sin(x2*tanh(x2)*t),1.2+.2*sin(x2*tanh(x2)*t)
    u=m*(-eta*tanh(s)-k*s-lam*de)+c*x2**2*tanh(x2)
    x1dot=x2
    x2dot=(1/m)*(u-c*x2**2*tanh(x2))
    return [x1dot,x2dot]

def solver(t0,y0,dt,t1,param):
    x,t=[[] for i in range(2)],[]
    r=ode(f).set_integrator('dopri5',method='bdf')
    r.set_initial_value(y0,t0).set_f_params(param)
    while r.successful() and r.t<t1:
        r.integrate(r.t+dt)
        for i in range(2):
            x[i].append(r.y[i])
        t.append(r.t)
    return x,t

if __name__=='__main__':
    t0,y0,dt,t1=0,[0,0],1e-2,10
    eta,k,lam=11.2,10,12
    param=[eta,k,lam]
    names=["x1","x2","control_profile"]
    x,t=solver(t0,y0,dt,t1,param)
    t=array(t)
    x1,x2=array(x[0]),array(x[1])
    e=x1-1
    de=x2
    s=de+lam*e
    m,c=3+1.5*sin(x2*tanh(x2)*t),1.2+.2*sin(x2*tanh(x2)*t)
    u=m*(-eta*tanh(s)-k*s-lam*de)+c*x2**2*tanh(x2)

    for i in range(3):
        if i!=2:
            plt.subplot(3,1,i+1)
            plt.plot(t,x[i],label=names[i])
            plt.legend(loc='upper right')
        else:
            plt.subplot(3,1,i+1)
            plt.plot(t,u,label=names[i])
            plt.legend(loc='upper right')

    plt.show()
