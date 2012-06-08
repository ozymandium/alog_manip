#!/usr/env/python

"""
usage of alog_manip utilities

Created 6/6/2012, by Robert Cofield
"""

#################################
### pulling out gNovatel data ###
#################################

import os, alog_manip
os.chdir('/home/gavlab/alog_manip/scripts') # where this module currently is
alogSrc = '/home/gavlab/alog_manip/alogs/short.alog'
alogTgt = '/home/gavlab/alog_manip/alogs/output.alog'
desStr = 'gNovatel'
alog_manip.pullByStr2new(alogSrc, alogTgt, desStr)


##################################