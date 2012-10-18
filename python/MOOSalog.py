#!/usr/bin/env python
"""
importing:
    from MOOSalog import MOOSalog       ... if using OOP supported functions
functions not converted to OOP probably won't work

Author: Robert Cofield
Created 6/6/2012
Python v2.7.3, using Ubuntu Precise (12.04)
"""

## from navpy:
# def getFloat(line):
#     return float(line.split()[-1])

# def getTimeStamp(line):
#     return float(line.split()[0])
from pprint import pprint
import time


################################################################################
##### Non - Class Files Used ###################################################

def reconstructLine(msgList):
    """
    INPUT msgList is a python list of length 4:
        time (string), zMeasurment (string), gSensor (string), value (string)

    OUTPUT will be a one-line string with no formatting characters

    typical (short enough variable names) spacing:
    |[col1]         |[col17]        |[col38]        |[col54]
    time(16cols)    meas(21cols)    sens(16cols)    valu(inf_cols)

    If one measurment is too long, the following parts are bumped back, even if they could have been inline correctly... fix this
    -this function not updated since transition to MOOSalog class
    """
    timeSpc = 16 # size allotted each of columns
    measSpc = 21
    sensSpc = 16

    time_short_enough = True
    meas_short_enough = True
    sens_short_enough = True

    time = msgList[0] #keep as string
    meas = msgList[1] 
    sens = msgList[2]
    valu = msgList[3] #keep as string

    time = str(round(float(time), 3))
    
    if len(time) >= timeSpc:
        time_short_enough = False
    if len(meas) >= measSpc:
        meas_short_enough = False
    if len(sens) >= sensSpc:
        sens_short_enough = False

    line = time
    if time_short_enough:
        line += (' '*(timeSpc-len(time)) + meas)
    else:
        line += (' ' + meas)

    if meas_short_enough:
        line += (' '*(measSpc-len(meas)) + sens)
    else:
        line += (' ' + sens)

    if sens_short_enough:
        line += (' '*(sensSpc-len(sens)) + valu)
    else:
        line += (' ' + valu)

    return line


################################################################################
################################################################################

class MOOSalog(object):
    """
    MOOSalog class
        inputs: srcf    => '/path/to/alog/source'
                outf    => '/path/to/resultant/alog'

    Ensure that there are no empty lines in the source file
    
    Class is designed to perform a single function, which populates outData,
    then be written to file. Subsequent actions require multiple instances.
    
    Time architecture not updated to work with string message values

    inputs: srcf    => '/path/to/alog/source'
                outf    => '/path/to/resultant/alog'
                arch    => currently 2 possiblities:
                    defaults to srcData[sensor][measurment][time] = value
                    'time' : srcData[time][sensor][measurment] = value
    
    """
    def __init__(self, srcf=None, outf=None, arch=None):
        super(MOOSalog, self).__init__()
        ##File & Data holder inits
        if srcf is not None:
            self.srcFileLoc = srcf # string
            self.srcFile = open(self.srcFileLoc, 'rU') # read from source file
            self.srcHeader = []
            self.srcData = dict()
        if outf is not None: # so this is going somewhere.
            self.outFileLoc = outf
            self.outFile = open(self.outFileLoc, 'w') # overwrites existing file (if any)
            self.outHeader = []
            self.outData = dict() # leave empty until told otherwise
            self.outData_temp = None
        ##Determine what data holder arch to use and read source alog
        self.arch = arch
        if self.arch == None:
            self.readSrc_bySens()
        elif self.arch == 'time':
            self.readSrc_byTime()  
        else:
            raise StandardError('arch type incorrect. see docstring')                    

    def closefiles(self):
        self.srcFile.close()
        self.outFile.close()


    # def setOutFile(self, outf):
    #     """ closes any existing output file, assigns new string to outFile"""
    #     try:
    #         self.outFile.close() # close present outfile if exists
    #     except: # it don't be there
    #         pass
    #     self.outFileLoc = outf
    #     self.outFile = open(self.outFileLoc, 'w') # overwrites
    #     self.outData = dict()


    def readSrc_bySens(self):
        """ Creates dictionary of source data
        !! Does not yet support attribute header storage !!
        Dictionary Structure:
            dctn['header']: list of each line containing '%%'
            dctn['gSensor']['zMeasurment'][Time] = value
        Note that no newline '\n' is present in data when using later.
        """
        dctn = self.srcData
        dctn['header'] = []
        # dctn['header'] = ['%% This dictionary created by alog_manip.alogrd_dict']
        for msg in self.srcFile: # broken by lines, are now strings
            msg = msg[0:-1] # remove \n at the end of the string
            if '%%' in msg:
                dctn['header'].append(msg) # assume all comments occur at beginning of file
            else:
                msg = msg.split()
                if msg[2] not in dctn: # none from this gSource yet
                    dctn[msg[2]] = {}
                if msg[1] not in dctn[msg[2]]: # none in this gSource from this zMeas yet
                    dctn[msg[2]][msg[1]] = {}
                try:
                    dctn[msg[2]][msg[1]][float(msg[0])] = float(msg[3]) # double
                except ValueError: # it's a string
                    # dimc = msg[3].split(']')[0].split('x')[1] # cols
                    # dimr = msg[3].split(']')[0].split('x')[0][1:] # rows
                    value_s = msg[3].split(']')[1][1:-1].split(',')
                    dctn[msg[2]][msg[1]][float(msg[0])] = [float(i) for i in value_s]
                except IndexError: # it's blank
                    dctn[msg[2]][msg[1]][float(msg[0])] = None # nan better?


    def readSrc_byTime(self):
        """ Creates dictionary of source data
        sends header to self.srcHeader: list of each line conaining '%%'
        Dictionary Structure:
            self.srcData[time]['sens']['meas'] = value
        """
        for msg in self.srcFile:
            msg = msg[0:-1] # remove \n at the end of the string
            if '%%' in msg:
                self.srcHeader.append(msg)
            else:
                msg = msg.split()
                time = float(msg[0])
                meas = msg[1]
                sens = msg[2]
                valu = msg[3]
                if time not in self.srcData: # none from this time yet
                    self.srcData[time] = {}
                if sens not in self.srcData[time]: # none at this time from this gSensor
                    self.srcData[time][sens] = {}
                self.srcData[time][sens][meas] = valu # assume only one message per meas from sens at a time


    ############################################################################
    ##### Functions to increase measage frequency ##############################
    def increaseFreq(self, desHz):
        """
        Note this function designed to work on original sens->meas->time based
        dictionary architecture.

        Given a dictionary of alog data, increases message frequency to scpecified rate via interpolation
        ***Assume all msgs occur in chronological order***

        linearly adds data between supplied datapoints - no recalculating given data
            -note this function created to have smoother visualizations from alog data, not to be used in any mathematical calculations (yet)
        yields time to 3 decimal places

        ### To finalize the calculations afterward: ###
        # self.makeChronList() # sort by time
        # self.writeChronListToFile #write to file
        # self.closefiles() # we're done
        """
        from scipy.interpolate import interp1d
        import time
        from numpy import linspace, floor
        from decimal import getcontext, Decimal

        if desHz > 1000: # set max freq here 
            raise ValueError('Max Frequency is 1000 (3 decimal places)')
        now = time.asctime(time.localtime(time.time()))    
        stamp = ''.join(['%% The following created by alog_manip.MOOSalog.MOOSalog.increaseFreq\n%% ', now])
        increase_msg = ''.join(['%% Resultant Frequency: ',str(desHz),' Hz'])
        # hiHz = {}
        self.outData = {} # erase pre-existing dict
        self.outData['header'] = [stamp,increase_msg,'%%%%'] + self.srcData['header']

        def create_msgs():
            """ Puts interpolated data into dict outData
            Primary interpolation function for increaseFreq
            Consider using uniaxial spline --> would have one function for all of dictionary dat
            """
            getcontext().prec = 3 # will round to 3 decimal places
            orig_times = sorted(dat)
            for n in range(len(dat) - 1):
                linfun = interp1d([orig_times[n], orig_times[n+1]], \
                                  [dat[orig_times[n]], dat[orig_times[n+1]]])
                dt = orig_times[n+1] - orig_times[n] # current
                freq = 1/dt # current
                if dt < (1/desHz):
                    print('found instance where Freq already at/above desired Freq')
                else:
                    new_dt = dt*freq/desHz
                    new_times = linspace(orig_times[n],orig_times[n+1],floor(dt/new_dt))
                    # print(new_times)
                    new_values = linfun(new_times)
                    # rounded_values = [float(Decimal("%.3f" % e)) for e in new_values]
                    rounded_times = [float(Decimal("%.3f" % e)) for e in new_times]
                    for m in range(len(rounded_times)):
                        # this_time = int(new_times[m]*100000)/100000 # 5 decimal places in timstamp
                        self.outData[sens][meas][rounded_times[m]] = new_values[m]

        ## go thru and pull out dictionaries {time: value} then send to interpolation func
        for sens in self.srcData:
            if sens is not 'header':
                self.outData[sens] = {}
                for meas in self.srcData[sens]:
                    self.outData[sens][meas] = {}
                    dat = self.srcData[sens][meas]
                    if len(dat) == 1:
                        self.outData[sens][meas] = dat # only 1 data point, no interp
                    else:
                        create_msgs()


    def makeChronList(self):
        """use after invoking increaseFreq
        saves self.outData_temp as 2-layer nested list:
            [[time, sens, meas, value]
             [time, sens, meas, value]]
        list order is chronological - 
        """
        from operator import itemgetter
        ## make list of msg lists in the format accespted by reconstructLine
        self.outData_temp = [] # this will be in chronological order
        for sens in self.outData:
            if sens is not 'header':
                for meas in self.outData[sens]:
                    for time in self.outData[sens][meas]:
                        value = self.outData[sens][meas][time]
                        thismsg = [time, sens, meas, str(value)] # leave time as float for sorting
                        self.outData_temp.append(thismsg)
        self.outData_temp.sort(key=itemgetter(0)) # sort by first index
        for msg in self.outData_temp: # now we can make time a string
            msg[0] = str(msg[0])


    def writeChronListToFile(self):
        """uses the output of makeChronList -- outData_temp -- to to generate
        alog lines with reconstructLine, then writes those to the outFileLoc, 
        after using the header from outData
        """
        ## write header
        for header_line in self.outData['header']:
            self.outFile.write(header_line + '\n')
        ##loop through each msg list
        for msg_list in self.outData_temp:
            ## create line
            msg_line = reconstructLine(msg_list)
            ## write to file
            self.outFile.write(msg_line + '\n')

##### End increaseFreq-related functions #######################################
################################################################################

    def get_tmin(self):
        """returns the earliest source data point time.
        Designed to work with timebased architectures.
        """
        tmin = min(sorted(self.srcData.keys()))
        return tmin


    def minimizeTimes(self):
        """subtracts the lowest existing timestamp value from all msg times
        Designed to work on time-based architectures.
        relies on get_tmin function.
        """
        from copy import deepcopy as dcp
        tmin = self.get_tmin()
        for t in self.srcData:       
            old = dcp(self.srcData[t])
            new_t = t - tmin
            self.outData[new_t] = old


    def writeOut(self):
        """ Writes the output file and closes all open files
        Time-based architectures only
        """
        # import time
        self.outHeader = self.srcHeader
        for line in self.outHeader:
            self.outFile.write(line + '\n')
        # now = time.asctime(time.localtime(time.time()))
        # self.outFile.write('%% -- %s -- Written to new alog' % now)
        for time_s in sorted(self.outData):
            for sens in self.outData[time_s]:
                for meas in self.outData[time_s][sens]:
                    valu = self.outData[time_s][sens][meas]
                    msg_list = [str(time_s), meas, sens, str(valu)]
                    line_string = reconstructLine(msg_list)
                    self.outFile.write(line_string + '\n') 


    def pullByStr2new(self, desStr): # not tested in OOP
        """
        finds msgs with a string in meas type or source and creates a separate *.alog file from those msgs

        INPUTS:
            alogSrc     ::  ABSOLUTE PATH STRING of source *.alog file
            alogTgt     ::  ABSOLUTE PATH STRING of desired target *.alog file
            desStr      ::  messages containing any STRING in this LIST will be copied

        -will overwrite alogTgt if already existing
        -this function not updated since transition to MOOSalog class
        """
        
        def extractData():
            """ iterator which finds given data
            yields msgs in list format which contain a desired string in the source (third) column

                -slave function to pullByStr2new

            src         ::  reader object from source *.alog file
            desStr      ::  string we're looking for
            -this function not updated since transition to MOOSalog class
            """
            for line in src:
                line = str(line) # now each line is a string
                line = line.rstrip()
                if '%%' in line: #header
                    yield line
                for desired in desStr:
                    if desired in line:
                        yield line

        src = self.srcFile
        tgt = self.outFile
        tgt.write('%% Generated by alog_manip.pullByStr2new\n')
        for desired in range(len(desStr)):
            desStr[desired] = ' ' + desStr[desired] + ' '
            #this keeps things like 'zLat' and 'zLatStdDev' from causing redundancies`
        for line in extractData():
            tgt.write(line + '\n')
        # src.close()
        # tgt.close()



################################################################################
######## All code below not yet updated to new object oriented implementation ##
################################################################################

    def replStr(alogSrc, alogDst, tgtStrs, desStrs):
        """
        in the *.alog source file at absolute path alogSrc, finds strings in list tgtStrs in either 2nd or 3rd columns and replaces them with corresponding string in list desStrs, then saves changes to *.alog destination file at absolute path alogDst
        -no changes made to the source file
        Note that output is not yet in pretty justified columns
        This needs to have more file I/O stuff - delete old file & write new?
        not working - consider using extractData and making it more robust
        -this function not updated since transition to MOOSalog class
        """
        import os

        curdir = os.getcwd()
        os.chdir('/')
        src = open(alogSrc, 'rU')
        dst = open(alogDst, 'w')
        os.chdir(curdir)
        dst.write('%% This file has been modified by alog_manip.replStr \n')
        for phrase in tgtStrs: # take care of possible name confusions (find too many targets)
            phrase = ' ' + phrase + ' '
        for phrase in desStrs:
            phrase = ' ' + phrase + ' '
        for msg in src:
            if '%%' in msg: #will be written with dblspc at the end of this for loop unless we take of the \n now
                msg = msg[0:-2]
            for ind in range(len(tgtStrs)): # use indices of inputs in case of lists
                if tgtStrs[ind] in msg: # bingo.
                    msg == msg.split(msg)
                    if msg[1] == tgtStrs[ind]: # its the measurement we're replacing
                        msg[1] = desStrs[ind]
                    elif msg[2] == tgtStrs[ind]: # its the sensor we're replacing
                        msg[2] == desStrs[ind]
                    else:
                        print('Warning:: Bad target string')
                    msg = reconstructLine(msg)
            dst.write(msg + '\n') # took \n off the non-reconstituted msgs (comments)

        src.close()
        dst.close()


    def makeNoisy(alogSrc, alogTgt, meas, mag):
        """
        Adds gaussian white noise to specific measurements in an *.alog file.

        INPUTS:
            alog        ::  ABSOLUTE PATH of *.alog file
            meas        ::  LIST of WHICH MEASUREMENT (z_______) to corrupt with gaussian noise
            mag         ::  LIST of std devs, corresponding to meas

        Note that output is not yet in pretty justified columns --> examine Create_alog.m to fix
        -this function not updated since transition to MOOSalog class

        Consider using a single vector of noise instead of new noise generation each iteration
        """
        import os
        from numpy.random import normal
        # if meas[0] != 'z':
        #     error()
        curdir = os.getcwd()
        os.chdir('/')
        src = open(alogSrc, 'rU')
        tgt = open(alogTgt, 'w')
        os.chdir(curdir)

        for msg in src:
            if ("%%" in msg):
                msg = msg[0:-2] # get rid of \n at end for printing later
            else:
                msg = msg.split()
                for des in range(len(meas)):
                    if msg[1] == meas[des]:
                        noise = normal(float(msg[3]), mag[des], 1)
                        msg[3] = str(noise[0]) # center deviation about measurement
                msg = reconstructLine(msg)
            # print(msg)

            tgt.write(msg + '\n')


    