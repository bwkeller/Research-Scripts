#!/usr/bin/python2.6
import pynbody
import copy
import numpy as np
from optparse import OptionParser
import matplotlib.pyplot as plt
import pynbody.plot.sph as sph
import pynbody.analysis.profile as profile

def test(array):
	inflow0 = np.zeros((10,2))#Thickness = 100 pc
	inflow1 = np.zeros((10,2))#Thickness = 100 pc
	inflow2 = np.zeros((10,2))#Thickness = 100 pc
	inflow3 = np.zeros((10,2))#Thickness = 100 pc
	inflow4 = np.zeros((10,2))#Thickness = 100 pc
	inflow5 = np.zeros((10,2))#Thickness = 100 pc
	radii = [0.1, 0.5, 1, 5, 10, 20, 30, 50, 80, 100]
	for i in range(len(radii)):
		(inflow0[i,0], inflow0[i,1]) = getinflow(array, radii[i], 0.01)
		(inflow1[i,0], inflow1[i,1]) = getinflow(array, radii[i], 0.1)
		(inflow2[i,0], inflow2[i,1]) = getinflow(array, radii[i], 0.5)
		(inflow3[i,0], inflow3[i,1]) = getinflow(array, radii[i], 1)
		(inflow4[i,0], inflow4[i,1]) = getinflow(array, radii[i], 5)
		(inflow5[i,0], inflow5[i,1]) = getinflow(array, radii[i], 10)
	plt.semilogy(radii, inflow0[:,0], 's', color='red', 
	label="10 pc thickness")
	plt.semilogy(radii, inflow1[:,0], 'o', color='orange', 
	label="100 pc thickness")
	plt.semilogy(radii, inflow2[:,0], '^', color='yellow',
	label="500 pc thickness")
	plt.semilogy(radii, inflow3[:,0], '+', color='green', 
	label="1 kpc thickness")
	plt.semilogy(radii, inflow4[:,0], '*', color='blue', 
	label="5 kpc thickness")
	plt.semilogy(radii, inflow5[:,0], 'p', color='violet', 
	label="10 kpc thickness")
	plt.legend()
	plt.xlabel(r"Radius $(kpc)$")
	plt.ylabel(r"Mass inflow $(M_\odot / yr)$")
	plt.show()
	plt.clf()
	plt.semilogy(radii, inflow0[:,1], 's', color='red', 
	label="10 pc thickness")
	plt.semilogy(radii, inflow1[:,1], 'o', color='orange', 
	label="100 pc thickness")
	plt.semilogy(radii, inflow2[:,1], '^', color='yellow',
	label="500 pc thickness")
	plt.semilogy(radii, inflow3[:,1], '+', color='green', 
	label="1 kpc thickness")
	plt.semilogy(radii, inflow4[:,1], '*', color='blue', 
	label="5 kpc thickness")
	plt.semilogy(radii, inflow5[:,1], 'p', color='violet', 
	label="10 kpc thickness")
	plt.legend()
	plt.xlabel(r"Radius $(kpc)$")
	plt.ylabel(r"Number of particles")
	plt.show()

#def bondiaccretion(arrayin, radius, thickness, alpha=1):
def getinflow(array, radius, thickness, alpha=1):
	mass_enc = 0
	starsprof_enc = profile.Profile(array.stars, ndim=3, nbins=1, 
	min="0 kpc", max=str(radius)+" kpc")
	gasprof_enc = profile.Profile(array.gas, ndim=3, nbins=1, 
	min="0 kpc", max=str(radius)+" kpc")
	gasprof = profile.Profile(array.gas, ndim=3, nbins=1, 
	min=str(radius)+" kpc",	max=str(radius+thickness)+" kpc")
	if gasprof_enc['n'] > 0:
		mass_enc += gasprof_enc['mass']
	if starsprof_enc['n'] > 0:
		mass_enc += starsprof_enc['mass']
	rho = gasprof['rho']
	c_s = gasprof['c_s']
	mdot = 4.0*np.pi*alpha*pynbody.units.G * pynbody.units.G * mass_enc * \
	mass_enc * rho / 	np.power(c_s, 3)
	mdot.convert_units("Msol yr^-1")
	return (mdot, gasprof['n'])

def hopkinsaccretion(arrayin, radius, thickness):
	array = copy.deepcopy(arrayin)
	mdot = 0
	#array['mdot'] = -1.0*array['mass']*array['vr']/array['r']
	array['mdot'] = -1.0*array['mass']*array['vr']/ \
	(thickness * pynbody.units.Unit("kpc"))
	starsprof = profile.Profile(array.stars, ndim=3, nbins=1, 
	min=str(radius)+" kpc",	max=str(radius+thickness)+" kpc")
	gasprof = profile.Profile(array.gas, ndim=3, nbins=1, 
	min=str(radius)+" kpc",	max=str(radius+thickness)+" kpc")
	if gasprof['n'] > 0:
		mdot += gasprof['mdot']
	if starsprof['n'] > 0:
		mdot += starsprof['mdot']
	mdot.convert_units("Msol yr^-1")
	return (mdot, gasprof['n']+starsprof['n'])

if __name__ == "__main__":
	usage="mass_inflow.py [options] radius thickness inputfile\n Units are all in kpc and Msol, and years"
	parser = OptionParser(usage=usage)
	(opts, args) = parser.parse_args()
	if len(args) != 3:
		print "Incorrect number of arguments.  See --usage for help"
		exit(1)
	radius = float(args[0])
	thickness = float(args[1])
	infile = pynbody.load(args[2])
	infile.physical_units()
	test(infile)
