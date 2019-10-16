#!/usr/bin/env python3
import matplotlib
matplotlib.use('QT4Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

plt.xkcd()

mean = 0
variance = 1
sigma = np.sqrt(variance)
x = np.linspace(0,3,100)
plt.plot(x,mlab.normpdf(x,mean,sigma))

plt.show()
