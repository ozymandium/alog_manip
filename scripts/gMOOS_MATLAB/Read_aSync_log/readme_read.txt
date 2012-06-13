This file should take in any '.alog' file  and automatically create the matlab structures
from the given device, message, and data values in the file.

If a string of data is provided, say from a lidar, you will get a data structure that
includes cells.  The way to acces your data, say the first set of angle data and plot 
it would be done with: plot(gIbeoAlascaXT.zAngleAlpha{1})
Note: it is using {} and not ().