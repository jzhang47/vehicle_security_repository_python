'''
input:	a file folder, which contains all driver files;
		under each driver file, there are 4 or more .xlsx files;
output:	.csv files, each file is one driver's all calculated data,
		file name is the driver's name 
function:extract data from raw data, and calculate, and gereate one .csv file for each driver;
		 delete folders that contain driver's data; 
'''

import xlrd
import csv
import os
import shutil
import math
import re


BEGIN_LINE_NUMBER = 5

TIMESTAMP_COLUM_NO = 0

POSITIONX_COLUM_NO = 1
POSITIONY_COLUM_NO = 2
POSITIONZ_COLUM_NO = 3

ROTATIONX_COLUM_NO = 4
ROTATIONY_COLUM_NO = 5
ROTATIONZ_COLUM_NO = 6
ROTATIONW_COLUM_NO = 7

SPEED_COLUM_NO = 8 
STEER_COLUM_NO = 9
GASPEDAL_COLUM_NO = 10
BRAKE_COLUM_NO = 11
ENGINE_COLUM_NO = 12
INTEREST_COLUM_NO = 13


sampling_interval = 200 # defaut sampling_interval
sampling_data = []  # store all datas only for one sample calculation
global_driver_name = []
            
def getExcelFileInfo(f):
    print "the current file is: ",f        
#    print "the current sheet name is:       ", sheet.name
#    print "the total rows in this sheet is: ", sheet.nrows
#    print "the total cols in this sheet is: ", sheet.ncols
#    print "the valid data will be from lineNo. : ", BEGIN_LINE_NUMBER 
    printFunctionName("getExcelFileInfo") 
    return 

def secondToMs(time_s):
    return time_s * 1000

def msToSecond(time_ms):
    return time_ms/1000
      
def markLine(sheet, interval_ms):
    lineNo_marked = []
    lineNo_marked.append(BEGIN_LINE_NUMBER)
    record = []
    sum = 0
    for index in range(BEGIN_LINE_NUMBER, sheet.nrows):
        sum += int(sheet.cell(index, TIMESTAMP_COLUM_NO).value) - int(sheet.cell(index-1, TIMESTAMP_COLUM_NO).value)
        if(sum < interval_ms):
            continue
        lineNo_marked.append(index+1)
        record.append(sum)
        sum = 0
    print "the marked line are:",lineNo_marked
    print "the length of marked line is ", len(lineNo_marked)
    print "the actual sampling_time is:",record
    printFunctionName("markLine")
    return lineNo_marked             
                   
def howManySamples(sheet, intervals_s):
    total_samples = 0
    sum = 0
    interval_ms = secondToMs(intervals_s)   
    for index in range(BEGIN_LINE_NUMBER, sheet.nrows):
        sum += int(sheet.cell(index, TIMESTAMP_COLUM_NO).value) - int(sheet.cell(index-1, TIMESTAMP_COLUM_NO).value)
        if(sum < interval_ms):
            continue
        total_samples += 1
        sum = 0
    print "the total number of samples will be: ", total_samples
    printFunctionName("howManySamples")
    return total_samples

def getStarLine(lineNo_marked, current_sample):
    return lineNo_marked[current_sample] - 1
        
def getEndLine(lineNo_marked, current_sample):
    return lineNo_marked[current_sample + 1] - 1
 
def getDataForOneSampling(start_line,end_line):
    data = []
    for row_index in range(start_line , end_line ):
        data.append(sheet.row_values(row_index) )
    print "the start line No.is: ",start_line + 1
    print "the end line No.is: ",end_line
    print "the total rows of data collected for one sampling is: ", len(data)
    printFunctionName("getDataForOneSampling")
    return data 

def calEuclidianDistance(start_pos_value, end_pos_value):
    #start_pos_value and end_pos_value should be like this [x1,y1,z1]
    sum = 0.0
    for i in range(len(start_pos_value)):
        sum += math.pow(end_pos_value[i]-start_pos_value[i],2)
    ds = math.sqrt(sum)
    return ds

def calDistanceTraveled():
    sum = 0.0
    for i in range(len(sampling_data)-1):
        start_pos_val = []  #[x1,y1,z1]
        end_pos_val = []    #[x2,y2,z2]
        start_pos_val.append(sampling_data[i][POSITIONX_COLUM_NO])
        start_pos_val.append(sampling_data[i][POSITIONY_COLUM_NO])
        start_pos_val.append(sampling_data[i][POSITIONZ_COLUM_NO])
        end_pos_val.append(sampling_data[i+1][POSITIONX_COLUM_NO])
        end_pos_val.append(sampling_data[i+1][POSITIONY_COLUM_NO])
        end_pos_val.append(sampling_data[i+1][POSITIONZ_COLUM_NO])                    
        sum += calEuclidianDistance(start_pos_val,end_pos_val)
    sum = float("{0:.5f}".format(sum))
    print "the total distance from start_line to end_line is: ", sum
    printFunctionName("calDistanceTraveled") 
    return sum
    
def calAvgSpeed():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][SPEED_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average speed is: ",avg 
    printFunctionName("calAvgSpeed") 
    return avg

def calStdDeviationOfSP():   
    value  = []
    for i in range(len(sampling_data)):
        value.append(sampling_data[i][STEER_COLUM_NO])
    stddev = stdDev(value)
    stddev = float("{0:.2f}".format(stddev))
    print "the standard deviation of steering position is:",stddev
    printFunctionName("calStdDeviationOfSP")
    return stddev  

def calAvgChangeOfBP():
    sum = 0.0
    length = len(sampling_data)
    for i in range(length - 1):        
        start_val = sampling_data[i][BRAKE_COLUM_NO]
        end_val = sampling_data[i+1][BRAKE_COLUM_NO]
        sum += abs(end_val- start_val)
    avg = sum*1.0/length 
    avg = float("{0:.2f}".format(avg))
    print "the average change in brake position is:", avg
    printFunctionName("calAvgChangeOfBP") 
    return avg    

def calAveChangeOfAP():
    sum = 0.0
    length = len(sampling_data)
    for i in range(length - 1):        
        start_val = sampling_data[i][GASPEDAL_COLUM_NO]
        end_val = sampling_data[i+1][GASPEDAL_COLUM_NO]
        sum += abs(end_val- start_val)
    avg = sum*1.0/length
    avg = float("{0:.2f}".format(avg))                   
    print "the average change in accelerator position is:", avg
    printFunctionName("calAveChangeOfAP") 
    return avg 
   
def calAvgOfPositionX():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][POSITIONX_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average position_X is: ",avg 
    printFunctionName("calAvgOfPositionX") 
    return avg

def calAvgOfPositionY():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][POSITIONY_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average position_Y is: ",avg 
    printFunctionName("calAvgOfPositionY") 
    return avg

def calAvgOfPositionZ():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][POSITIONZ_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average position_Z is: ",avg 
    printFunctionName("calAvgOfPositionZ") 
    return avg

def calAvgOfRotationX():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][ROTATIONX_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average rotation_X is: ",avg 
    printFunctionName("calAvgOfRotationX") 
    return avg
    
def calAvgOfRotationY():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][ROTATIONY_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average rotation_Y is: ",avg 
    printFunctionName("calAvgOfRotationY") 
    return avg

def calAvgOfRotationZ():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][ROTATIONZ_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average rotation_Z is: ",avg 
    printFunctionName("calAvgOfRotationZ") 
    return avg

def calAvgOfRotationW():
    sum = 0.0
    for i in range(len(sampling_data)):
        sum += sampling_data[i][ROTATIONW_COLUM_NO]
    avg = sum/len(sampling_data)
    avg = float("{0:.2f}".format(avg)) 
    print "the average rotation_W is: ",avg 
    printFunctionName("calAvgOfRotationW") 
    return avg

def mean(value):
    return sum(value)*1.0/len(value)

def stdDev(value):
    length = len(value)
    m = mean(value)
    total_sum = 0
    for i in range(length):
        total_sum += (value[i]-m) **2
    under_rood = total_sum *1.0/length
    return math.sqrt(under_rood)

def printFunctionName(name):
    print "-----THIS IS THE END OF FUNCTION:", name,"-----"
    return

def saveAsCSV(d,result):
    #file_name = f.replace(".xlsx", ".csv") 
    file_name = d +".csv"
    csvfile = file(file_name, 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(result)
    csvfile.close()
    print "the data is saved to file:",file_name
    printFunctionName("**********saveAsCSV**********")
    
def getCurDirectory():
    file_dict =  {}
    #file_list = []
    cur_dir = os.getcwd()
    for folder in os.walk(cur_dir).next()[1]:
        f = os.path.join(cur_dir, folder)
        for filename in os.walk(f).next()[1]:
            global_driver_name.append(filename)
            file_path = os.path.join(f, filename)
            temp = []
            for i in os.walk(file_path).next()[2]:
                abs_file_path = os.path.join(file_path, i)
                #file_list.append(abs_file_path)
                temp.append(abs_file_path)
            file_dict[file_path] = temp
    print file_dict.keys()
    printFunctionName("getCurDirectory")
    return file_dict

def getDriverName(f):
    name = "null"
    temp = f.split('/')
    name = temp[-2]
    return name 
            
def getDriverNo(f):
    driverno = -1;
    temp = f.split('/')
    name = temp[-2]
    for i in range(len(global_driver_name)):
        if ( name == global_driver_name[i]):
            return i
    return driverno
 
def getFromWhichFile(f):
    fileno = -1;
    t =  f.split('/')
    temp = t[-1][::-1]
    m = re.search('[0-9]',temp)
    fileno = m.group(0)
    print "the current file number is :", fileno
    return fileno
 
def delXlsFile(f):
    os.remove(f)
    printFunctionName("delXlsFile")
                   
if __name__== '__main__':    
    sampling_interval = input('Enter a sampling interval time(in second): ')
    file_dict = getCurDirectory()
    print "the drivers here are:\n", global_driver_name
    for d in file_dict:
        print "dirctory is :", d
        result = []
        header = ["DriverName",
                  "DriverNo",
                  "FromWhichFile",
                  "DistanceTraveled", 
                  "AvgSpeed",
                  "StdDeviationOfSteerPos",
                  "AvgChangeOfBrakePos",
                  "AvgChangeOfAccelaratePos",
                  "AvgPositionX",
                  "AvgPositionY",
                  "AvgPositionZ",
                  "AvgRotationX",
                  "AvgRotationY",
                  "AvgRotationZ",
                  "AvgRotationW",]
        result.append(header)
        for f in file_dict[d]:
            print "current file is:", f
            book = xlrd.open_workbook(f)
            sheet = book.sheet_by_index(0)        
            getExcelFileInfo(f)
            sample_count = howManySamples(sheet, sampling_interval)
            lineNo_marked = markLine(sheet, secondToMs(sampling_interval))
            for i in range(sample_count):
                oneSample = []
                sampling_data = getDataForOneSampling(getStarLine(lineNo_marked, i),getEndLine(lineNo_marked, i))
                oneSample.append(getDriverName(f))
                oneSample.append(getDriverNo(f))
                oneSample.append(getFromWhichFile(f))           
                oneSample.append(calDistanceTraveled())        
                oneSample.append(calAvgSpeed())
                oneSample.append(calStdDeviationOfSP())
                oneSample.append(calAvgChangeOfBP())
                oneSample.append(calAveChangeOfAP())
                oneSample.append(calAvgOfPositionX())
                oneSample.append(calAvgOfPositionY())
                oneSample.append(calAvgOfPositionZ())
                oneSample.append(calAvgOfRotationX())
                oneSample.append(calAvgOfRotationY())
                oneSample.append(calAvgOfRotationZ())
                oneSample.append(calAvgOfRotationW())
                result.append(oneSample)
            delXlsFile(f)
        saveAsCSV(d,result)
        shutil.rmtree(d)
    print "this is the end!"