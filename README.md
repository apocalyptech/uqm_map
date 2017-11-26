Ur-Quan Masters / Star Control II Starmap Viewer
================================================

This project is an initial runup to porting my UQM Starmap Viewer from
PyGTK (and Python 2) to PyQt5 (and Python3).  The current PyGTK version
is available here:

    http://apocalyptech.com/uqm/

Its sourcecode repository was never actually made public, just living as
a local CVS repository on my home server, and I've decided not to bother
importing the history to this Git repo, since it'll nearly entirely be
a rewrite anyway.

At time of writing, the only parts of the project to be imported here are
the data classes, which have been reworked somewhat (so they're no longer
compatible with the data classes used in the released app), and I've got
those 100% unit tested.  Hopefully work on the actual PyQt5 components
will begin shortly, but for the meantime, don't expect this to be a working
project.

Once this project is actually usable as an app, I'll update the README
with some more pertinent information.  For now, though, if you're looking
for a working starmap viewer for UQM/SC2, just check out the main 
project page and content yourself with Py2/PyGTK.
