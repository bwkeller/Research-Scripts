#!/usr/bin/python
import re
import envoy
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser

if __name__ == "__main__":
	cbarlabel = ""
	normalized = False
	log = True
	parser = OptionParser()
	(options, args) = parser.parse_args()
	if len(args) < 1:
		print "No gasoline log specified"
		exit(1)
	logfile = args[0]
	script = "#!/bin/bash\necho 0.00000 >> tmpfile\ncat %s | grep 'distribution\|Forces' | grep -B1 'distribution' | grep -v '\-' | sed -e 's/Forces, Step://' | sed -e 's/nActive.*//' | sed -e 's/Rung distribution: (//' | sed -e 's/)//' >> tmpfile" % logfile
	scriptfile = open('tmpscript', 'w')
	scriptfile.write(script)
	scriptfile.close()
	envoy.run("chmod +x tmpscript")
	envoy.run("./tmpscript")
	envoy.run("rm tmpscript")
	runglines = open("tmpfile").readlines()
	timesteps = []
	rungs = []
	for i in range(len(runglines)):
		if i%2 == 0:
			timesteps.append(runglines[i])
		else:
			rungs.append([float(i) for i in runglines[i].split(',')])
	rungs = np.array(rungs)
	if normalized:
		rungs /= np.sum(rungs[0])
	rungs = np.flipud(np.rot90(rungs))
	if log:
		rungs = np.log10(rungs)
		cbarlabel = "log10 "
	if normalized:
		cbarlabel += "Normalized "
	cbarlabel += "Particle Count"
	plt.imshow(rungs, aspect='auto', interpolation='nearest', origin='lower')
	cbar = plt.colorbar()
	cbar.set_label(cbarlabel)
	plt.ylabel('Rung')
	plt.xlabel('Timestep')
	plt.yticks(range(20))
	plt.grid(xdata=np.arange(len(runglines)))
	plt.show()
	envoy.run('rm tmpfile')
