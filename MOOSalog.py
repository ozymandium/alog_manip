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

    if len(time) >= timeSpc:
        time_short_enough = False
    if len(meas) >= measSpc:
        meas_short_enough = False
    if len(sens) >= sensSpc:
        sens_short_enough

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


class MOOSalog(object):
    """
    MOOSalog class
        inputs: src     => '/path/to/alog/source'
                outf    => '/path/to/resultant/alog'
    """
    def __init__(self, srcf, outf=None):
        super(MOOSalog, self).__init__()
        self.srcFileLoc = srcf # string
        self.srcFile = open(self.srcFileLoc, 'rU') # read from source file
        self.srcData = dict()
        self.mkdict() # read to self.srcData

        if outf is not None: # so this is going somewhere.
            self.outFileLoc = outf
            self.outFile = open(self.outFileLoc, 'w') # overwrites existing file (if any)
            self.outData = dict() # leave empty until told otherwise
            self.outData_temp = None
    

    def closefiles(self):
        self.srcFile.close()
        self.outFile.close()


    # def empty(self):
        # pass


    def setOutFile(self, outf):
        """ closes any existing output file, assigns new string to outFile"""
        try:
            self.outFile.close() # close present outfile if exists
        except: # it don't be there
            pass
        self.outFileLoc = outf
        self.outFile = open(self.outFileLoc, 'w') # overwrites
        self.outData = dict()


    def mkdict(self):
        """ Creates dictionary of data upon __init__
        Dictionary Structure:
            dctn['header']: list of each line containing '%%'
            dctn['gSensor']['zMeasurment'][Time] = value
        Presently assumes that 4th column (value) is convertible to float
            -need to make it dance with lidar strings
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
                dctn[msg[2]][msg[1]][float(msg[0])] = float(msg[3])


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


    def increaseFreq(self, desHz):
            """
            Given a dictionary of alog data, increases message frequency to scpecified rate via interpolation
            ***Assume all msgs occur in chronological order***

            linearly adds data between supplied datapoints - no recalculating given data
                -note this function created to have smoother visualizations from alog data, not to be used in any mathematical calculations (yet)
            yields time to 3 decimal places
            """
            from scipy.interpolate import interp1d
            import time
            from numpy import linspace, floor
            from decimal import getcontext, Decimal

            if desHz > 1000: # set max freq here 
                raise ValueError('Max Frequency is 1000 (3 decimal places)')
            now = time.asctime(time.localtime(time.time()))    
            stamp = ''.join(['%% The following was created by alog_manip.MOOSalog.increaseFreq on ', now])
            increase_msg = ''.join(['%% Resultant Frequency: ',str(desHz),' Hz'])
            # hiHz = {}
            self.outData = {} # erase pre-existing dict
            self.outData['header'] = [stamp,increase_msg,'%%%%'] + self.srcData['header']

            # global sens, meas, dat # reexamine this later

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

            # go thru and pull out dictionaries {time: value} then send to interpolation func
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


    def find_t0(self):
        """finds the earliest time in outData_temp"""
        if self.outData_temp is None:
            self.outData_temp = self.outData
            wasnone = True
        t0 = None
        for sens in self.outData_temp:
            for meas in self.outData_temp[sens]:
                t0_thismeas = sorted(self.outData_temp[sens][meas])[0]
                if t0 is None:
                    t0 = t0_thismeas # if this is the first iter, just use lowest value
                elif t0 > t0_thismeas:
                    t0 = t0_thismeas
        if wasnone:
            self.outData_temp = None
        return t0


    def get_t0_msgs(self):
        """returns a list of msg lists in the format accepted by reconstructLine which are stamped with the t0
        """
        if self.outData_temp is None:
            self.outData_temp = copy.deepcopy(self.outData)
            wasnone = True
        t0 = self.find_t0()
        t0_msglist = []
        for sens in self.outData_temp:
            for meas in self.outData_temp[sens]:
                if t0 in self.outdata_temp[sens][meas]:
                    value = pop(self.outdata_temp[sens][meas][t0])
                    msg = [str(t0), sens, meas, str(value)]
                    t0_msglist.append(msg)
        if wasnone:
            self.outData_temp = None


    def get_sorted_msglist(self):

    # def chronologize(self):
    #     """time-order"""
    #     self.outData_temp = copy.deepcopy(self.outData) # want non-referenced
    #     msgs = []
    #     for sens in self.outData:
    #         for meas in self.outData[sens]:
    #             times = sorted(self.outData[sens][meas]):
    #             valus = []
    #             for time in times:
    #                 valus.append = self.outData[sens][meas][time]
    #                 msgs.append([str(time), sens, meas, str(valu)])
    #     return msgs


    #     sens_firsts = getSensFirsts()
    #     pprint(sens_firsts)



###############################################################################################
############ All code below not yet updated to new object oriented implementation #############
###############################################################################################

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


    