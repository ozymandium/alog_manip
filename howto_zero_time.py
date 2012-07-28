#!/usr/bin/env python
"""
zeros the alog from scott's data
"""

from MOOSalog import MOOSalog

file_loc = '/home/ozymandium/MATLAB/Leader_Follower_GUI_data/ScottSimLF.alog'
out_loc = '/home/ozymandium/alog_Files/ScottSimLF_zeroed.alog'
alog = MOOSalog(file_loc, out_loc)
alog.minimizeTimestamps()
alog.closefiles()