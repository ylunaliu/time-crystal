import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from pylab import *

def f1(x, a, b,c):
    return a*np.exp(-b*x) + c

# def f1(x, a, b, c, d):
#     return a*np.exp(-c*(x-b))+d

data= np.load("/Users/luna/Documents/GitHub/Time-crystal-qiskit/threethings.npy",allow_pickle=True)
# data3= np.load("/Users/luna/Documents/GitHub/Time-crystal-qiskit/g=0.6.npy",allow_pickle=True)
data_097 = data[:30]
data_006 = data[30:60]
data_echo = data[60:75]
avg = np.sum(data_097[:2])/2
# print(avg)
# data2 = np.array(list((filter(lambda x: x>avg, data_097))))
# print(data2)
x= np.arange(0,30)
x2 = np.arange(0, 30, 2)
print(f"this is {x2}")

popt, pcov = scipy.optimize.curve_fit(f1, x2, data_echo) 
print(popt)
y_fit2 = f1(x,*popt)
odd = []
even = []
counter = 0
for i, datapoint in enumerate(y_fit2):
    
    if(i%2==0):
        even.append(data_echo[counter])
        print(data_echo [counter])
        counter+=1
        print(counter)
    else:
        even.append(-datapoint)
print(f"here is even{even} and odd{odd}")

plt.plot(x,data_097, '-bo', label = "g=0.97")
# plt.plot(x2, data_echo)
plt.plot(x, even, 'ro', label="y = {:.2f}exp(-{:.2f}x) + {:.2f}".format(popt[0], popt[1], popt[2]))
plt.plot(x,data_006,'-go', label = "g=0.6")
plt.legend()
plt.show()