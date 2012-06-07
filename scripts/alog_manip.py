#!/usr/bin/python
"""
collection of functions for manipulating *.alogs

Author: Robert Cofield
Created 6/6/2012
Python v2.7.3
"""

#############################################################################################


def filtered_alog(alog_file, gDes):
    for line in alog_file:
        line = line.strip()
        line = line.split(',')
        if len(line) != 4:
            print("Bad line")
            continue
        result = []
        result.append(float(line[0]))
        result.append(line[0])
        result.append(line[0])
        result.append(float(line[0]))
        if gDes in result[2]:
            yield result


def pull_source(alogSrc, alogTgt, gDes):
    """
    finds msgs from  a specified source(s) and creates a separate *.alog file from those msgs


    INPUTS:
        alogSrc     ::  absolute filename of source *.alog file
        alogTgt     ::  absolute filename of desired target *.alog file
        gDes        ::  string name of instrument(s) from which desired measurements come

    """
    import csv, os

    curdir = os.getcwd()

    # read source alogs
    os.chdir('/')
    src_rd = csv.reader(open(alogSrc))
    for line in filtered_alog(src_rd, gDes):
        pass


###########################################################################################


def agwn(alogSrc, alogTgt, meas):
    """
    Adds gaussian white noise to specific measurements in an *.alog file.
    """
    import csv, os

    curdir = os.getcwd()