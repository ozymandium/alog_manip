#!/usr/env/python

"""
usage of alog_manip utilities

	-demonstration script, with small/useless files for testing only

Created 6/6/2012, by Robert Cofield
"""

import os, alog_manip
os.chdir('/home/gavlab/alog_manip/scripts') # where this module currently is

############################################
### pulling out & muddying gNovatel data ###
############################################

alogSrc = '/home/gavlab/alog_manip/alogs/short.alog'
alogTgt = '/home/gavlab/alog_manip/alogs/output_uncor.alog'
desStr = ['gNovatel']
alog_manip.pullByStr2new(alogSrc, alogTgt, desStr)


### making specific gNovatel meas noisy ###
meas = 'zcourse'
alogSrc = '/home/gavlab/alog_manip/alogs/output_uncor.alog'
alogTgt = '/home/gavlab/alog_manip/alogs/output_corr.alog'
meas = ['zCourse', 'zVertVel']
mag = [2.5, .0001]
alog_manip.makeNoisy(alogSrc, alogTgt, meas, mag)


###################################################
### saving an alog file as a pickled dictionary ###
###################################################

alogfile = '/home/gavlab/alog_manip/alogs/short.alog'
dctn = alog_manip.alogrd_dict(alogfile)
print(dctn)