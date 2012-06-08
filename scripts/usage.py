#!/usr/env/python

"""
usage of alog_manip utilities
"""


import os
print
os.chdir('/home/gavlab/alog_manip/scripts') # where this module currently is
from alog_manip import *
alogSrc = '/home/gavlab/alog_manip/alogs/short.alog'
alogTgt = None
gDes = 'gNovatel'

pullSrc2new(alogSrc, alogTgt, gDes)