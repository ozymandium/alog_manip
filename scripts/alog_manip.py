#!/usr/bin/python
"""
collection of functions for manipulating *.alogs

Author: Robert Cofield
Created 6/6/2012
Python v2.7.3
"""

#############################################################################################


def pullByStr2new(alogSrc, alogTgt, desStr):
    """
    finds msgs with a string in meas type or source and creates a separate *.alog file from those msgs

    INPUTS:
        alogSrc     ::  absolute path of source *.alog file
        alogTgt     ::  absolute path of desired target *.alog file
        desStr      ::  messages containing this string will be copied

    """
    import csv, os

    curdir = os.getcwd()
    os.chdir('/') # go to root so that reader can use abs pathname
    src_rd = csv.reader(open(alogSrc), delimiter='\n') # read source alogs
    writer = open(alogTgt, 'w')
    os.chdir(curdir)
    # origHead = [] # header of the original *.alog
    # newData = [] # contains the string we're looking for 
    
    for line in filterData(src_rd, desStr):
        writer.write(line[2:-2] + '\n')


def filterData(alog_rd, desStr):
    """
    yields msgs in list format which contain a desired string in the source (third) column

    alog_rd     ::  reader object from source *.alog file
    desStr      ::  string we're looking for
    """

    for line in alog_rd:
        line = str(line) # now each line is a string
        line = line.rstrip()
        if (desStr in line) or ('%%' in line): #header
            yield line


###########################################################################################
### Toolkit for 
###########################################################################################

def agwn(alogSrc, alogTgt, meas):
    """
    Adds gaussian white noise to specific measurements in an *.alog file.
    """
    import csv, os

    curdir = os.getcwd()