#!/usr/bin/python

### make copies with only novatel data
import os
os.chdir('/home/gavlab/alog_manip/scripts')
import alog_manip

alogSrc = '/home/gavlab/alog_manip/alogs/fhwa2_long.alog'
alogTgts = ['/home/gavlab/alog_manip/alogs/fhwa2_Novatel_corr_01.alog',
		    '/home/gavlab/alog_manip/alogs/fhwa2_Novatel_corr_02.alog',
		    '/home/gavlab/alog_manip/alogs/fhwa2_Novatel_corr_03.alog']
desStr = ['zLat', 'zLong', 'zLatStdDev', 'zLongStdDev', 'zCourse']

for alogTgt in alogTgts:
	alog_manip.pullByStr2new(alogSrc, alogTgt, desStr) # create desired signals-only

#####

meas = ['zLat', 'zLong', 'zLatStdDev', 'zLongStdDev', 'zCourse']
mag = 