'''
input:	  xlsx files whose folder is in the same directory with this .py file
output:   xlsx files whose file names are the same as the input ones	
function: change float datas in xlsx files to 2-decimal points;
          change negative data into positive one
          change coordinate from (x,y,z) to (x', y', z')  
'''

import xlrd
import xlwt
import csv
import os
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
             
def getCurDirectory():
    file_dict =  {}
    #file_list = []
    cur_dir = os.getcwd()
    for folder in os.walk(cur_dir).next()[1]:
        f = os.path.join(cur_dir, folder)
        for filename in os.walk(f).next()[1]:
            file_path = os.path.join(f, filename)
            temp = []
            for i in os.walk(file_path).next()[2]:
                abs_file_path = os.path.join(file_path, i)
                #file_list.append(abs_file_path)
                temp.append(abs_file_path)
            file_dict[file_path] = temp
    print file_dict.keys()
    return file_dict


def minInCol(col):
    '''
    the col is like [???, ???, ???, ???, 34, ...]
    '''
    for times in range(4):
        del col[0]  # delete first 4 elements of col
    rs = min(col)
    return rs 

def processDataFromSingleFile(f):
    rows_data = []
    book = xlrd.open_workbook(f)
    sheet = book.sheet_by_index(0)

    pos_x_min = minInCol(sheet.col_values(POSITIONX_COLUM_NO))
    pos_y_min = minInCol(sheet.col_values(POSITIONY_COLUM_NO))
    pos_z_min = minInCol(sheet.col_values(POSITIONZ_COLUM_NO))
    rota_x_min = minInCol(sheet.col_values(ROTATIONX_COLUM_NO))
    rota_y_min = minInCol(sheet.col_values(ROTATIONY_COLUM_NO))
    rota_z_min = minInCol(sheet.col_values(ROTATIONZ_COLUM_NO))
    rota_w_min = minInCol(sheet.col_values(ROTATIONW_COLUM_NO))

    rows_data.append(sheet.row_values(0))   
    rows_data.append(sheet.row_values(1))
    rows_data.append(sheet.row_values(2))
    rows_data.append(sheet.row_values(3))
    for i in range(4,sheet.nrows): # 
        temp = []
        temp.append(int(sheet.cell(i,0).value))
        temp.append(float("{0:.2f}".format(sheet.cell(i,POSITIONX_COLUM_NO).value - pos_x_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,POSITIONY_COLUM_NO).value - pos_y_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,POSITIONZ_COLUM_NO).value - pos_z_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,ROTATIONX_COLUM_NO).value - rota_x_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,ROTATIONY_COLUM_NO).value - rota_y_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,ROTATIONZ_COLUM_NO).value - rota_z_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,ROTATIONW_COLUM_NO).value - rota_w_min)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,SPEED_COLUM_NO).value)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,STEER_COLUM_NO).value + 1))) # change from [-1, 1] to [0, 2] 
        temp.append(float("{0:.2f}".format(sheet.cell(i,GASPEDAL_COLUM_NO).value)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,BRAKE_COLUM_NO).value)))
        temp.append(float("{0:.2f}".format(sheet.cell(i,ENGINE_COLUM_NO).value)))
        rows_data.append(temp)
    return rows_data 
 
def saveFile(filePath,result):
    file = xlwt.Workbook() 
    table = file.add_sheet(filePath.split("/")[-1])
    for i in range(len(result)):
        for j in range(len(result[i])):
                table.write(i,j,result[i][j])
    file.save(filePath)
    print "----#####file has saved to ", filePath

if __name__== '__main__':    
    file_dict = getCurDirectory()
    for d in file_dict:
        print "dirctory is :", d
        for f in file_dict[d]:
            print "----current file is:", f
            all_data = processDataFromSingleFile(f)
            #print all_data
            os.remove(f) 
            saveFile(f,all_data)
    print "this is the end!"

    
