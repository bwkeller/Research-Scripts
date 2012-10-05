#!/usr/bin/python
from sys import argv
import struct

if __name__ == "__main__":
	f = open(argv[1], 'r+b')
	newt = float(argv[2])
	t, n, ndim, ng, nd, ns = struct.unpack("diiiii", f.read(28))
	newhead = struct.pack("diiiii", newt, n, ndim, ng, nd, ns)
	f.seek(0)
	f.write(newhead)
	f.close()
