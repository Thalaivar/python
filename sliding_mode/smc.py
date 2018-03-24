import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import ode
from numpy import sin, cos, tan, tanh
from mpl_toolkits.mplot3d import Axes3D

DEG_TO_RAD = 0.0174533

PHI = 0
THETA = 1
PSI = 2

Ix = (0.000081599 + 0.00032233 + 0.0133609 + 0.0044966)
Iy = (0.000586590 + 0.00032233 + 0.0133609 + 0.0044966)
Iz = (0.000621150 + 0.00032968 + 0.0163521 + 0.0118809)

u_x = []
u_y = []
u_z = []

def model(t, X, params):

    phi, theta, psi, wx, wy, wz, ie_wx, ie_wy, ie_wz= X

    kp = params[0]
    eta = params[1]
    l = params[2]

    # get desired attitude
    if t > 4:
        desired_attitude = np.array([40, -10, 0])
    else:
        desired_attitude = np.array([0, 0, 0])
    attitude = np.array([phi, theta, psi])

    # error in desired attitude
    e_angle = attitude - desired_attitude

    # desired body rates
    w_d = -e_angle*kp

    # controller error
    w = np.array([wx, wy, wz])

    e = w - w_d

    # sliding surfaces
    sx = Ix*e[0] + l[0]*ie_wx
    sy = Iy*e[1] + l[1]*ie_wy
    sz = Iz*e[2] + l[2]*ie_wz

    # controller outputs
    ux = (Iz - Iy)*wy*wz - l[0]*e[0] - eta[0]*tanh(sx)
    uy = (Ix - Iz)*wx*wz - l[1]*e[1] - eta[1]*tanh(sy)
    uz = (Iy - Ix)*wy*wx - l[2]*e[2] - eta[2]*tanh(sz)

    u_x.append(ux)

    # return dot vector
    attitude = attitude*DEG_TO_RAD

    phi_dot = wx + sin(attitude[PSI])*tan(attitude[THETA])*wy + cos(attitude[PSI])*tan(attitude[THETA])*wz
    theta_dot =  cos(attitude[PSI])*wy - sin(attitude[PSI])*wz
    psi_dot = (sin(attitude[PSI])/cos(attitude[THETA]))*wy + (cos(attitude[PSI])/cos(attitude[THETA]))*wz
    wx_dot = (1/Ix)*(ux - (Iz - Iy)*wy*wz)
    wy_dot = (1/Iy)*(uy - (Ix - Iz)*wx*wz)
    wz_dot = (1/Iz)*(uz - (Iy - Ix)*wx*wy)
    ie_wx_dot = e[0]
    ie_wy_dot = e[1]
    ie_wz_dot = e[2]

    return [phi_dot, theta_dot, psi_dot, wx_dot, wy_dot, wz_dot, ie_wx_dot, ie_wy_dot, ie_wz_dot]

def main(kp, eta, l):

    t1 = 10
    t0 = 0
    dt = 0.005

    X0 = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    x = np.zeros((2000, 9))
    t = []

    params = [kp, eta, l]

    r = ode(model).set_integrator('dopri5', method='bdf')
    r.set_initial_value(X0, t0).set_f_params(params)

    i = 0
    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        x[i] = r.y
        t.append(r.t)
        i = i + 1

    return x, t

if __name__ == '__main__':

    kp = [1.54, 1.54, 1.54]
    eta = [0.21, 0.01, 0.01]
    l = [0.04, 0.04, 0.04]

    x, t = main(kp, eta, l)

    phi = np.reshape(x[:,0], (2000,))
    theta = np.reshape(x[:,1], (2000,))
    psi = np.reshape(x[:,2], (2000,))

    wx = np.reshape(x[:,3], (2000,))
    wy = np.reshape(x[:,4], (2000,))
    wz = np.reshape(x[:,5], (2000,))

    ie_wx = np.reshape(x[:,6], (2000,))
    ie_wy = np.reshape(x[:,7], (2000,))
    ie_wz = np.reshape(x[:,8], (2000,))

    angles = [phi, theta, psi]
    u = [ux, uy, uz]

    for i in range(3):
        plt.subplot(3, 1, i+1)
        plt.plot(u[i])
        plt.grid();

    plt.show()
