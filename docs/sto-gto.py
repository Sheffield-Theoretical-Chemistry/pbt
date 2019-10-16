#!/usr/bin/env python3
# Plots a comparison of 1s STO and GTO 
import matplotlib
matplotlib.use('QT4Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.xkcd()

x = np.linspace(0,4,100)
plt.plot(x, np.exp(-x), color="red")
plt.plot(x, np.exp(-x**2), color="blue")

ax = plt.gca() # Gets current axis
ax.spines['right'].set_color('none') # Hide the right spines (boundary area)
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom') # x-axis ticks on bottom only
ax.yaxis.set_ticks_position('left')
ax.set_xlabel('RADIUS')
ax.set_ylabel('AMPLITUDE')
ax.text(2.75, 0.65, 'PYTHON\nBASIS\nTOOL', fontsize=30)

plt.annotate('STO', xy=(2.0, np.exp(-2.0)), arrowprops=dict(arrowstyle='->'), xytext=(2.25, 0.275))
plt.annotate('GTO', xy=(0.57, np.exp(-0.57**2)), arrowprops=dict(arrowstyle='->'), xytext=(0.82, 0.85))

plt.show()
