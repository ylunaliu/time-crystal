from email.errors import UndecodableBytesDefect
import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt


# H = -d^2/dx^2 + V
# V(x) = V0 * Random(x)

# define some constants
dt = 0.01 # time step
N = 300 # Number of x-points (numerical discretization)
L = 10 # system size [-L,L]
V0 = 20 # strength of disorder
sigma = 1 # gaussian width of the initial wavefunction configuration
x = np.linspace(-L,L,N)
dx = x[1] - x[0] # x value spacing

# define gaussian wavefunction
psi0 = np.exp(-x**2/(2*sigma**2))
# normalize wavefunction
psi0 = psi0 /  np.sqrt( dx * np.sum(psi0**2) )

# define -d^2/dx^2
# f'(x) = (f(x+ dx/2) - f(x - dx/2) ) / dx
# f''(x) = ((f(x+dx) - 2*f(x) + f(x-dx))) / dx**2
H = -(np.diag(np.ones(N-1),1) + np.diag(np.ones(N-1),-1) - 2* np.diag(np.ones(N))) / dx**2

np.random.seed(1)
V = V0 * np.diag(np.random.rand(N))

Uclean = expm( - 1j * dt * H)
Udisorder = expm( - 1j * dt * (H + V))

#%%
psiclean = np.copy(psi0)
psidisorder = np.copy(psi0)

#%%
plt.plot(x, np.abs(psi0)**2, label='clean')
plt.xlim((-L,L))
plt.xlabel('$x$')
plt.ylabel('$|\Psi|^2$')

#%%
%matplotlib qt
plt.ion()
for i in range(600):
    psiclean = Uclean@psiclean
    psidisorder = Udisorder@psidisorder
    plt.clf()
    plt.plot(x, np.abs(psiclean)**2, label='clean')
    plt.plot(x, np.abs(psidisorder)**2, label='disordered')
    plt.ylim(0,1)
    plt.xlim((-L,L))
    plt.xlabel('$x$')
    plt.ylabel('$|\Psi|^2$')
    plt.legend()
    plt.pause(0.07)

plt.close('all')

#%%
plt.clf()
plt.plot(x, np.diag(V))