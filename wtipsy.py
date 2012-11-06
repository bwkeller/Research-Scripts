import struct
import numpy as np
def wtipsy(filename, header, catg, catd, cats, STANDARD=True):
	try:
		f = open(filename, 'wb')
	except:
		print "WTIPSY ERROR: Can't open file"
		return 1
	f.write(struct.pack("<diiiii", header['time'], header['n'], header['ndim'], header['ngas'], header['ndark'], header['nstar']))
	for i in range(header['ngas']):
		f.write(struct.pack("<ffffffffffff", catg['mass'][i], catg['x'][i], catg['y'][i], catg['z'][i], catg['vx'][i], catg['vy'][i], 
			catg['vz'][i], catg['dens'][i], catg['tempg'][i], catg['h'][i], catg['zmetal'][i], catg['phi']))
	for i in range(header['ndark']):
		f.write(struct.pack("<fffffffff", catd['mass'][i], catd['x'][i], catd['y'][i], catd['z'][i], catd['vx'][i], catd['vy'][i], 
			catd['vz'][i], catd['eps'][i], catd['phi']))
	for i in range(header['nstar']):
		f.write(struct.pack("<fffffffffff", cats['mass'][i], cats['x'][i], cats['y'][i], cats['z'][i], cats['vx'][i], cats['vy'][i], 
			cats['vz'][i], cats['metals'][i], cats['tform'][i], cats['eps'][i], cats['phi']))
	f.close()
