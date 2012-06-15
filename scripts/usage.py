#!/usr/env/python

"""
usage of alog_manip utilities

	-demonstration script, with small/useless files for testing only

Created 6/6/2012, by Robert Cofield
"""

import os, alog_manip, shutil, sys
os.chdir('/home/gavlab/alog_manip/scripts') # where this module currently is

# ############################################
# ### pulling out & muddying gNovatel data ### This section works
# ############################################

# alogSrc = '/home/gavlab/alog_manip/alogs/short.alog'
# alogTgt = '/home/gavlab/alog_manip/alogs/output_uncor.alog'
# desStr = ['gNovatel']
# alog_manip.pullByStr2new(alogSrc, alogTgt, desStr)

# ### making specific gNovatel meas noisy ###
# meas = 'zcourse'
# alogSrc = '/home/gavlab/alog_manip/alogs/output_uncor.alog'
# alogTgt = '/home/gavlab/alog_manip/alogs/output_corr.alog'
# meas = ['zCourse', 'zVertVel']
# mag = [2.5, .0001]
# alog_manip.makeNoisy(alogSrc, alogTgt, meas, mag)


# ##############################################################
# ### saving an alog file as a pickled dictionary, reopening ### It works
# ##############################################################

# print('\n--The pickling test--\n')
# alogfile = '/home/gavlab/alog_manip/alogs/short.alog'
# dctn = alog_manip.alogrd_dict(alogfile)
# os.chdir('/home/gavlab/alog_manip/alogs')

# # pickle the dictionary - not yet tested
# import pickle
# prot = 2 # highest protocol @ time of writing
# output = open('/home/gavlab/alog_manip/alogs/short_dict,pkl', 'wb') # must specify open as binary with write permissions
# pickle.dump(dctn, output, prot)

# # open the pickle and see if it worked
# output.close()
# import pprint
# del dctn, output
# pkl_file = open('/home/gavlab/alog_manip/alogs/short_dict,pkl', 'rb') # always open as binary in case it wasn't in ASCII
# dctn = pickle.load(pkl_file)
# pkl_file.close()


#######################################
### rename certain phrases(strings) ### this section not yet tested
#######################################

alogSrc = '/home/gavlab/alog_manip/alogs/short.alog'
alogDst = '/home/gavlab/alog_manip/alogs/short_restring.alog'

tgtStrs = ['zVertVel','zHorizSpeed','zCourse']
desStrs = ['zVV','zHS','zC']

alog_manip.replStr(alogSrc, alogDst, tgtStrs, desStrs)

print('\n\nThis is the rename test -- open file short_restring.alog\n\n')