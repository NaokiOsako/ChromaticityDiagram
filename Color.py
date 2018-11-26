#coding: utf-8
from scipy import signal, interpolate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

lst = pd.read_csv("sample3.csv").values

X = np.array(lst[:,1])
Y = np.array(lst[:,2]) 
Z = np.array(lst[:,3])

node = 100

array = np.array([[0.4898, 0.3101, 0.2001],
                  [0.1769, 0.8124, 0.0107],
                  [0.0000, 0.0100, 0.9903]])

InvArray = np.linalg.inv(array)

        
x = X/(X + Y + Z)
y = Y/(X + Y + Z)
z = Z/(X + Y + Z)

xs, ys, zs = 0, 0, 0
tmpx =np.linspace(x[0], x[-1], node)
tmpy =np.linspace(y[0], y[-1], node)

for i in range(len(x)):
    xs += x[i]
    ys += y[i]
    zs += z[i]
    
XWhite = xs/(xs + ys + zs)
YWhite = ys/(xs + ys + zs)

Allx, Ally, AllX, AllZ = [], [], [], []

x = np.append(x, tmpx)
y = np.append(y, tmpy)

for (v, v2) in zip(x, y):
    tmpx =np.linspace(XWhite, v, node)
    Allx = np.append(Allx, tmpx)
    tmpy =np.linspace(YWhite, v2, node)
    Ally = np.append(Ally, tmpy)

AllY = Ally + 0.7 * np.exp(-(Allx-XWhite)**2 / 4000 - (Ally-YWhite)**2 / 4000)
AllX = Allx/Ally*AllY
AllZ = (1-Allx-Ally)/Ally*AllY

XYZ = [[x,y,z] for (x,y,z) in zip(AllX,AllY,AllZ)]
RGB = [np.dot(InvArray,v) for v in XYZ]
for v in RGB:
    if(v[0]<0):
        v[0] = 0
    if(v[0]>1):
        v[0] = 1
    if(v[1]<0):
        v[1] = 0
    if(v[1]>1):
        v[1] = 1     
    if(v[2]<0):
        v[2] = 0
    if(v[2]>1):
        v[2] = 1
        
plt.figure()
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
leg = plt.legend(loc=1, fontsize=25)
# leg.get_frame().set_alpha(1)
plt.scatter(Allx, Ally, marker='o', c=RGB)
plt.show()
