#!/usr/bin/python

import re
from sys import argv
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
	dSecUnit = float(re.search('(dSecUnit:) (\S+)', open(argv[1]).read()).group(2))
	dErgUnit = float(re.search('(dErgPerGmUnit:) (\S+)', open(argv[1]).read()).group(2))*float(re.search('(dMsolUnit:) (\S+)', open(argv[1]).read()).group(2))*1.998e33
	gaslog = [[float(j) for j in i.split()] for i in open(argv[1]).readlines() if i[0] != '#']
	dTime = np.array([i[0] for i in gaslog])*dSecUnit/3.1557e13
	E = np.array([i[2] for i in gaslog])*dErgUnit
	T = np.array([i[3] for i in gaslog])*dErgUnit
	U = np.array([i[4] for i in gaslog])*dErgUnit
	Eth = np.array([i[5] for i in gaslog])*dErgUnit
	plt.semilogx(dTime, E)
	plt.xlabel("Time (Myr)")
	plt.ylabel("Energy (Erg)")
	plt.show()
