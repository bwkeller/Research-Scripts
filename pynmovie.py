#!/usr/bin/python
import pynbody
import envoy
from optparse import OptionParser
import pynbody.analysis.angmom as angmom
import pynbody.plot.sph as p_sph
import matplotlib.pyplot as plt

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-r", "--range", action="store", dest="valrange", 
	help="The range of values to plot (in the format 'min max')")
	parser.add_option("-t", "--type", action="store", dest="ptype", 
	help="Type of particles to show (gas, dm, or star)", default="gas")
	(opts, args) = parser.parse_args()
	imgcount = 0
	fname = "pynmovie_"+opts.ptype+".mp4"
	try:
		(vmin, vmax) = [float(i) for i in opts.valrange.split()]
	except AttributeError:
		(vmin, vmax) = (None, None)
	for i in args:
		sim = pynbody.load(i)
		ptypes = {"gas":sim.gas, "dm":sim.dm, "stars":sim.stars}
		p_sph.image(ptypes[opts.ptype], cmap="hot", units="Msol kpc^-2", vmin=vmin, vmax=vmax)
		plt.savefig("%09d.png" % (imgcount))
		imgcount += 1
	vid = envoy.run('ffmpeg  -b 1800 -r 5 -i %09d.png '+fname)
	for i in range(imgcount):
		envoy.run("rm %09d.png" % (i))
