#pynmovie: The pynbody movie maker#
##Movie Scripts##
One of my favourite features for pynmovie is the script feature.  Called by
using the -e option, it will load the script specified on the command line, and
then, for each file, it processes the simulation using the scripts process(sim,
num) method.  This way, each simulation can be manipulated in a certain way, and
even have different plotting options used for each simulation based on where in
the sequence of files it is.  This makes it super easy to do things like
rotate/crop/transform the simulation prior to plotting, and to have the plotted
image change as movie runs (things like zooming and panning).
