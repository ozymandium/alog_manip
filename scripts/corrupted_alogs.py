#!/usr/bin/python

### make copies with only novatel data
import os
os.chdir('/home/gavlab/alog_manip/scripts')
import alog_manip

alogSrc = '/home/gavlab/alog_manip/alogs/fhwa2_long.alog'
alogTgts = ['/home/gavlab/alog_manip/alogs/fhwa2_Novatel_01.alog',
		    '/home/gavlab/alog_manip/alogs/fhwa2_Novatel_02.alog',
		    '/home/gavlab/alog_manip/alogs/fhwa2_Novatel_03.alog']
desStr = 'gNovatel'

for alogTgt in alogTgts:
	alog_manip.pullByStr2new(alogSrc, alogTgt, desStr)