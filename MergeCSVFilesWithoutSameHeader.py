'''
input:  .csv files in one dirctory
output:  delete all *.csv files in that directory;
         generate one csv file named with all_drivers.csv 
'''

import pandas as pd
import glob
import os

def concatnate():
	interesting_files = glob.glob("*.csv")
	df_list = []
	for filename in sorted(interesting_files):
		df_list.append(pd.read_csv(filename))
		full_df = pd.concat(df_list)
		full_df.to_csv('all_drivers.csv')
		os.remove(filename)	

if __name__== '__main__':
	concatnate()

