#!/usr/bin/python
"""
collection of functions for manipulating *.alogs

Author: Robert Cofield
Created 6/6/2012
Python v2.7.3
"""

#############################################################################################


def pullSrc2new(alogSrc, alogTgt, gDes):
    """
    finds msgs from  a specified source(s) and creates a separate *.alog file from those msgs

    INPUTS:
        alogSrc     ::  absolute path of source *.alog file
        alogTgt     ::  absolute path of desired target *.alog file
        gDes        ::  string name of instrument(s) from which desired measurements come

    """
    import csv, os

    curdir = os.getcwd()
    os.chdir('/') # go to root so that reader can use abs pathname
    src_rd = csv.reader(open(alogSrc)) # read source alogs
    os.chdir(curdir)
    origHead = []
    
    for line in filterBySrc(src_rd, gDes):
        # deal with header here - 1st 5 lines, begin with 2 percent signs
        if '%%' in line:
            origHead.append(line)
        else if 

        print(line)
        print('     new msgs        ')
        pass


def filterBySrc(alog_rd, gDes):
    """
    yields msgs in list format which contain a desired string in the source (third) column

    alog_rd     ::  reader object from source *.alog file
    gDes        ::  asdf
    """
    
    for line in alog_rd:
        print(line)
        # line = float(line)
        # line = line.strip()
        # line = line.split(',')
        # if len(line) != 4:
        #     print("Bad line") # may need to reconsider if using ibeo measurements (values?)
        #     continue
        
        # result = []
        # result.append(float(line[0])) # time
        # result.append(line[0]) # measurement name will already be a string
        # result.append(line[0]) # source name will already be a string
        # result.append(float(line[0])) # measured value
        
        # if gDes in result[2]:
        #     yield result


###########################################################################################
### Toolkit for 

def agwn(alogSrc, alogTgt, meas):
    """
    Adds gaussian white noise to specific measurements in an *.alog file.
    """
    import csv, os

    curdir = os.getcwd()