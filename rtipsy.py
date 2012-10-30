import struct
import numpy as np
def rtipsy(file, VERBOSE=False):
  """rtipsy Reads tipsy files detecting the format: 
  big endian, little endian, padded (standard) or non-padded header 
  
  Usage: 
          rtipsy(filename, VERBOSE=False)
  
  Input parameters: 
    filename  filename string
    VERBOSE  print messages (optional)
  Return values:
    (header,g,d,s)
    header    tipsy header struct
    g,d,s     gas, dark and star structures
  Please read rtipsy.py for the structure definitions
  
  Example: 
	h,g,d,s = rtipsy('/home/wadsley/usr5/mihos/mihos.std')
    print, h['ndark']
	plt.plot(d['x'], d['y'], 'k,')"""
  return
	try:
		f = open(file, 'rb')
	except:
		print "RTIPSY ERROR: Can't open file"
		return 1
	fs = len(f.read())
	f.seek(0)
	#Read in the header
	t, n, ndim, ng, nd, ns = struct.unpack("<diiiii", f.read(28))
	endianswap = False
	#Check Endianness
	if (ndim < 1 or ndim > 3):
		endianswap = True
		f.seek(0)
		t, n, ndim, ng, nd, ns = struct.unpack(">diiiii", f.read(28))
		if VERBOSE:
			print "SWAP_ENDIAN"
	if VERBOSE:
		print "Read time,n,ngas,ndark,nstar: ", t, n, ngas, ndark, nstar
	#Catch for 4 byte padding
	if (fs == 32+48*ng+36*nd+44*ns):
		f.read(4)
	#File is borked if this is true
	elif (fs != 28+48*ng+36*nd+44*ns):
		print "RTIPSY ERROR: Header and file size inconsistent"
		print "Estimates: Header bytes:  28 or 32 (either is OK)"
		print "     ngas: ",ng," bytes:",48*ng
		print "    ndark: ",nd," bytes:",36*nd
		print "    nstar: ",ns," bytes:",44*ns
		print "Actual File bytes:",fs,"  not one of:",28+48*ng+36*nd+44*ns,32+48*ng+36*nd+44*ns
		f,close()
		return 1
	catg = {'mass':np.zeros(ng), 'x':np.zeros(ng), 'y':np.zeros(ng), 'z':np.zeros(ng), 'vx':np.zeros(ng), 'vy':np.zeros(ng), 
			'vz':np.zeros(ng), 'dens':np.zeros(ng), 'tempg':np.zeros(ng), 'h':np.zeros(ng), 'zmetal':np.zeros(ng), 
			'phi':np.zeros(ng)}
	catd = {'mass':np.zeros(nd), 'x':np.zeros(nd), 'y':np.zeros(nd), 'z':np.zeros(nd), 'vx':np.zeros(nd), 'vy':np.zeros(nd), 
			'vz':np.zeros(nd), 'eps':np.zeros(nd), 'phi':np.zeros(nd)}
	cats = {'mass':np.zeros(ns), 'x':np.zeros(ns), 'y':np.zeros(ns), 'z':np.zeros(ns), 'vx':np.zeros(ns), 'vy':np.zeros(ns), 
			'vz':np.zeros(ns), 'metals':np.zeros(ns), 'tform':np.zeros(ns), 'eps':np.zeros(ns), 'phi':np.zeros(ns)}
	if (ng > 0):
		for i in range(ng):
			if endianswap:
				mass, x, y, z, vx, vy, vz, dens, tempg, h, zmetal, phi = struct.unpack("<ffffffffffff", f.read(48))
			else:
				mass, x, y, z, vx, vy, vz, dens, tempg, h, zmetal, phi = struct.unpack(">ffffffffffff", f.read(48))
			catg['mass'][i] = mass
			catg['x'][i] = x
			catg['y'][i] = y
			catg['z'][i] = z
			catg['vx'][i] = vx
			catg['vy'][i] = vy
			catg['vz'][i] = vz
			catg['dens'][i] = dens
			catg['tempg'][i] = tempg
			catg['h'][i] = h
			catg['zmetal'][i] = zmetal
			catg['phi'][i] = phi
	if (nd > 0):
		for i in range(nd):
			if endianswap:
				mass, x, y, z, vx, vy, vz, eps, phi = struct.unpack("<fffffffff", f.read(36))
			else:
				mass, x, y, z, vx, vy, vz, eps, phi = struct.unpack(">fffffffff", f.read(36))
			catd['mass'][i] = mass
			catd['x'][i] = x
			catd['y'][i] = y
			catd['z'][i] = z
			catd['vx'][i] = vx
			catd['vy'][i] = vy
			catd['vz'][i] = vz
			catd['eps'][i] = eps
			catd['phi'][i] = phi
	if (ns > 0):
		for i in range(ns):
			if endianswap:
				mass, x, y, z, vx, vy, vz, metals, tform, eps, phi = struct.unpack("<fffffffffff", f.read(44))
			else:
				mass, x, y, z, vx, vy, vz, metals, tform, eps, phi = struct.unpack(">fffffffffff", f.read(44))
			cats['mass'][i] = mass
			cats['x'][i] = x
			cats['y'][i] = y
			cats['z'][i] = z
			cats['vx'][i] = vx
			cats['vy'][i] = vy
			cats['vz'][i] = vz
			cats['metals'][i] = metals
			cats['tform'][i] = tform
			cats['eps'][i] = eps
			cats['phi'][i] = phi
	header = {'time':t, 'n':n, 'ndim':ndim, 'ngas':ng, 'ndark':nd, 'nstar':ns}
	return (header,catg,catd,cats)
