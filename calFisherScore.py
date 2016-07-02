'''
input : CSV files; 
		each CSV file contains all data of one driver;
		each CSV file contains 14 or 15 features that are generated from raw data;
output: print the fisherscore  
'''
import csv
import os
import math
import numpy as np

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
    for i in file_list:
        print i
    return file_list

def toFloat(ls):
    rs = []
    for i in ls:
        rs.append(float(i))
    return rs  

def getDataFromSingleFile(filename):
    rs = []
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
        print "the current file is :", filename
        readCSV = csv.reader(csvfile, delimiter= ',')
        headers = next(readCSV)
        for row in readCSV:
        	distance_travelled.append(row[DISTANCE_COLUM_NO])
        	avg_speed.append(row[AVG_SPEED_COLUM_NO])
        	std_deviation_sp.append(row[STD_DEVIATION_SP_COLUM_NO])
        	avg_change_bp.append(row[AVG_CHANGE_BP_COLUM_NO])
        	avg_change_ap.append(row[AVG_CHANGE_AP_COLUM_NO])
        	avg_position_x.append(row[AVG_POSITION_X_COLUM_NO])
        	avg_position_y.append(row[AVG_POSITION_Y_COLUM_NO])
        	avg_position_z.append(row[AVG_POSITION_Z_COLUM_NO])
        	avg_rotation_x.append(row[AVG_ROTATION_X_COLUM_NO])
        	avg_rotation_y.append(row[AVG_ROTATION_Y_COLUM_NO])
        	avg_rotation_z.append(row[AVG_ROTATION_Z_COLUM_NO])
        	avg_rotation_w.append(row[AVG_ROTATION_W_COLUM_NO])
    distance_travelled = toFloat(distance_travelled)
    avg_speed = toFloat(avg_speed)
    std_deviation_sp = toFloat(std_deviation_sp)
    avg_change_bp = toFloat(avg_change_bp) 
    avg_change_ap = toFloat(avg_change_ap)
    avg_position_x = toFloat(avg_position_x)
    avg_position_y = toFloat(avg_position_y)
    avg_position_z = toFloat(avg_position_z)
    avg_rotation_x = toFloat(avg_rotation_x)
    avg_rotation_y = toFloat(avg_rotation_y)
    avg_rotation_z = toFloat(avg_rotation_z)
    avg_rotation_w = toFloat(avg_rotation_w)
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
    a = np.asarray(rs)
    return a

def calWithinClassVar(v):
    return np.var(v)
        
def fisherScore(v,sumOfWithinCVar):
    print "the v is :", v
    print "the sumOfWithinCVar is :", sumOfWithinCVar
    print "the np.var(v) is:", np.var(v)
    print "the len(v) is :", len(v)
    return math.sqrt(len(v)*np.var(v)/math.pow(sumOfWithinCVar,2))
    #return math.sqrt(len(v) * np.var(v))/sumOfWithinCVar   
     
if __name__== '__main__':  
    feature_distance_travelled_12person = []
    feature_avg_speed_12person = []
    feature_std_deviation_sp_12person = []
    feature_avg_change_bp_12person = []
    feature_avg_change_ap_12person = []    
    feature_avg_position_x_12person = []
    feature_avg_position_y_12person = []
    feature_avg_position_z_12person = []
    feature_avg_rotation_x_12person = []
    feature_avg_rotation_y_12person = []
    feature_avg_rotation_z_12person = []
    feature_avg_rotation_w_12person = []    
    person_list = getCurDirectory()
    total_person = len(person_list)
    sigma = [] #[[feature_1,feature_2, ...], [feature_1, feature_2, ...], ...]
    for i in person_list:
        features = getDataFromSingleFile(i)
        feature_distance_travelled_12person.append(np.mean(features[FEATURE_DS]))
        feature_avg_speed_12person.append(np.mean(features[FEATURE_AVG_SPEED]))
        feature_std_deviation_sp_12person.append(np.mean(features[FEATURE_DEVIATION_SP]))
        feature_avg_change_bp_12person.append(np.mean(features[FEATURE_CHANGE_BP])) 
        feature_avg_change_ap_12person.append(np.mean(features[FEATURE_CHANGE_AP]))
        feature_avg_position_x_12person.append(np.mean(features[FEATURE_AVG_POSITION_X]))
        feature_avg_position_y_12person.append(np.mean(features[FEATURE_AVG_POSITION_Y]))
        feature_avg_position_z_12person.append(np.mean(features[FEATURE_AVG_POSITION_Z]))
        feature_avg_rotation_x_12person.append(np.mean(features[FEATURE_AVG_ROTATION_X]))
        feature_avg_rotation_y_12person.append(np.mean(features[FEATURE_AVG_ROTATION_Y]))
        feature_avg_rotation_z_12person.append(np.mean(features[FEATURE_AVG_ROTATION_Z]))
        feature_avg_rotation_w_12person.append(np.mean(features[FEATURE_AVG_ROTATION_W]))
        for j in range(len(features)):
            sigma.append(calWithinClassVar(features[j]))
    a = np.asarray(sigma)
    a = np.reshape(a,(-1,len(features))) #cut a array into a matrix, each coulum represents one feature 
    sumSigma = np.sum(a, axis=0)
    print "the sum of sigma is: \n", sumSigma
    print "the fish score of distance travelled is:               ",fisherScore(feature_distance_travelled_12person, sumSigma[FEATURE_DS])
    print "the fish score of average speed is:                    ",fisherScore(feature_avg_speed_12person,sumSigma[FEATURE_AVG_SPEED])
    print "the fish score of std deviation of steer position is:  ",fisherScore(feature_std_deviation_sp_12person,sumSigma[FEATURE_DEVIATION_SP])
    print "the fish score of avg change of brake position is;     ",fisherScore(feature_avg_change_bp_12person,sumSigma[FEATURE_CHANGE_BP]) 
    print "the fish score of avg change of accelarate position is:",fisherScore(feature_avg_change_ap_12person,sumSigma[FEATURE_CHANGE_AP])
    print "the fish score of avg position_x is:                   ",fisherScore(feature_avg_position_x_12person,sumSigma[FEATURE_AVG_POSITION_X])
    print "the fish score of avg position_y is:                   ",fisherScore(feature_avg_position_y_12person,sumSigma[FEATURE_AVG_POSITION_Y])
    print "******************************"
    print "the fish score of avg position_z is:                   ",fisherScore(feature_avg_position_z_12person,sumSigma[FEATURE_AVG_POSITION_Z])
    print "the fish score of avg rotation_x is:                   ",fisherScore(feature_avg_rotation_x_12person,sumSigma[FEATURE_AVG_ROTATION_X])
    print "the fish score of avg rotation_y is:                   ",fisherScore(feature_avg_rotation_y_12person,sumSigma[FEATURE_AVG_ROTATION_Y])
    print "the fish score of avg rotation_z is:                   ",fisherScore(feature_avg_rotation_z_12person,sumSigma[FEATURE_AVG_ROTATION_Z])
    print "the fish score of avg rotation_w is:                   ",fisherScore(feature_avg_rotation_w_12person,sumSigma[FEATURE_AVG_ROTATION_W])
    print "this is the end. "           
        
  
    

    
