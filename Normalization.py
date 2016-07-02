'''
input : one CSV file; 
output: the same CSV file in which all data are normalized;  
'''
import csv
import os
import math
import numpy as np

DRIVER_NAME_COLUM_NO = 0
DRIVER_NO_COLUM_NO = 1
FROM_WHICHFILE_COLUM_NO = 2
DISTANCE_COLUM_NO = 3
AVG_SPEED_COLUM_NO = 4
STD_DEVIATION_SP_COLUM_NO = 5
AVG_CHANGE_BP_COLUM_NO = 6
AVG_CHANGE_AP_COLUM_NO = 7
AVG_POSITION_X_COLUM_NO = 8
AVG_POSITION_Y_COLUM_NO = 9
AVG_POSITION_Z_COLUM_NO = 10
AVG_ROTATION_X_COLUM_NO = 11
AVG_ROTATION_Y_COLUM_NO = 12
AVG_ROTATION_Z_COLUM_NO = 13
AVG_ROTATION_W_COLUM_NO = 14

FEATURE_DS = 0
FEATURE_AVG_SPEED = 1
FEATURE_DEVIATION_SP = 2
FEATURE_CHANGE_BP = 3
FEATURE_CHANGE_AP = 4
FEATURE_AVG_POSITION_X = 5
FEATURE_AVG_POSITION_Y = 6
FEATURE_AVG_POSITION_Z = 7
FEATURE_AVG_ROTATION_X = 8
FEATURE_AVG_ROTATION_Y = 9
FEATURE_AVG_ROTATION_Z = 10
FEATURE_AVG_ROTATION_W = 11
        
def getCurDirectory():
    file_list = []
    cur_dir = os.getcwd()
    for folder in os.walk(cur_dir).next()[1]:
        f = os.path.join(cur_dir, folder)
        for filename in os.walk(f).next()[2]:
            file_path = os.path.join(f, filename)
            file_list.append(file_path)
    return file_list

def normalization_case1(v):
    if (v.max() == v.min()):
        return v
    return (v-v.min())/(v.max()-v.min())

def arrayToList(v):
	l = []
	for i in v:
		i = round(i,4)
		l.append(i)
	return l

def normalization_case2(v): # aband, and will not be used for minus number could be shown in v
    l = []
    A = np.log(v+1)
    for i in A:
    	l.append(i)
    return l

def getDataFromSingleFile(filename): 
    rs = [] #exclude the header
    driver_name =[]
    driver_no = []
    from_which_file = []
    distance_travelled = []
    avg_speed = []
    std_deviation_sp = []
    avg_change_bp = []
    avg_change_ap = []
    avg_position_x = []
    avg_position_y = []
    avg_position_z = []
    avg_rotation_x = []
    avg_rotation_y = []
    avg_rotation_z = []
    avg_rotation_w = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter= ',')
        headers = next(readCSV)
        for row in readCSV:
            driver_name.append(row[DRIVER_NAME_COLUM_NO])
            driver_no.append(row[DRIVER_NO_COLUM_NO])
            from_which_file.append(float(row[FROM_WHICHFILE_COLUM_NO]))
            distance_travelled.append(float(row[DISTANCE_COLUM_NO]))
            avg_speed.append(float(row[AVG_SPEED_COLUM_NO]))
            std_deviation_sp.append(float(row[STD_DEVIATION_SP_COLUM_NO]))
            avg_change_bp.append(float(row[AVG_CHANGE_BP_COLUM_NO]))
            avg_change_ap.append(float(row[AVG_CHANGE_AP_COLUM_NO]))
            avg_position_x.append(float(row[AVG_POSITION_X_COLUM_NO]))
            avg_position_y.append(float(row[AVG_POSITION_Y_COLUM_NO]))
            avg_position_z.append(float(row[AVG_POSITION_Z_COLUM_NO]))
            avg_rotation_x.append(float(row[AVG_ROTATION_X_COLUM_NO]))
            avg_rotation_y.append(float(row[AVG_ROTATION_Y_COLUM_NO]))
            avg_rotation_z.append(float(row[AVG_ROTATION_Z_COLUM_NO]))
            avg_rotation_w.append(float(row[AVG_ROTATION_W_COLUM_NO]))
   	rs.append(driver_name)
    rs.append(driver_no)
    rs.append(from_which_file)
    rs.append(distance_travelled)
    rs.append(avg_speed)
    rs.append(std_deviation_sp)
    rs.append(avg_change_bp)
    rs.append(avg_change_ap)
    rs.append(avg_position_x)
    rs.append(avg_position_y)
    rs.append(avg_position_z)
    rs.append(avg_rotation_x)
    rs.append(avg_rotation_y)
    rs.append(avg_rotation_z)
    rs.append(avg_rotation_w)
    return rs # rs = [..., [x1,x2,x3, ...], [y1,y2,y3, ...], [z1,z2,z3, ...], ...]   
              # x is one feature, y is another feature 

def savaAsCSV(person_path , data):
    file_name = person_path.split(".")[0] +"_Normalized.csv"
    csvfile = file(file_name, 'wb')
    writer = csv.writer(csvfile)
    header = header = ["DriverName",
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
    writer.writerow(header)
    for i in range(len(data[0])):
    	onerow = []
    	onerow.append(data[0][i])
    	onerow.append(data[1][i])
    	onerow.append(data[2][i])
    	onerow.append(data[3][i])
    	onerow.append(data[4][i])
    	onerow.append(data[5][i])
    	onerow.append(data[6][i])
    	onerow.append(data[7][i])
    	onerow.append(data[8][i])
    	onerow.append(data[9][i])
    	onerow.append(data[10][i])
    	onerow.append(data[11][i])
    	onerow.append(data[12][i])
    	onerow.append(data[13][i])
    	onerow.append(data[14][i])
    	writer.writerow(onerow)
    csvfile.close()
    print "the data is saved to file:",file_name

if __name__== '__main__': 
    result = []    
    person_list = getCurDirectory()
    total_person = len(person_list)
    for person_path in person_list:
    	print "the current person is:", person_path
        data = getDataFromSingleFile(person_path)
        for i in range(3, len(data)): # data[0],data[1],data[2] will not be used
        	v = normalization_case1(np.array(data[i]))
        	data[i] = arrayToList(v)
    	savaAsCSV(person_path,data)
        os.remove(person_path)
