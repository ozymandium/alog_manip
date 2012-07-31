#!/usr/bin/env python
"""
This script used to interpolate msgs from generated dummy inputs, creating msgs at ~100Hz
"""

import sys
sys.path.append('/home/gavlab/')
from alog_manip.MOOSalog import MOOSalog
from pprint import pprint

lo_file = '/home/gavlab/alog_Files/short.alog'
hi_file = '/home/gavlab/alog_Files/short_hiHz.alog'
desHz = 3
alog = MOOSalog(lo_file, hi_file)
alog.increaseFreq(desHz)
alog.makeChronList()
alog.writeChronListToFile()
alog.closefiles()