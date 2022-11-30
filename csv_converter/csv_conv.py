# -*- coding: utf-8 -*-

import csv
from os import listdir
from os.path import isfile, join
import numpy as np
import re


read_path = '..\\csv_converter\\input\\'
write_path = '..\\csv_converter\\output\\'
only_files = [f for f in listdir(read_path) if isfile(join(read_path, f))]

def mutateCsv(read_path, write_path):
	newData = ""
	times = {}
	with open(read_path, "r", encoding='unicode_escape') as fileread, open(write_path, "w", newline='', encoding='utf-8') as filewrite:
		data = fileread.read()
		writer = csv.writer(filewrite)

		for line in data.splitlines():
			#print(line)
			if re.match("^[0-9]+(\.[0-9]+)?\,-?[0-9]+(\.[0-9]+)?\,-?[0-9]+(\.[0-9]+)?\,?$", line):
				params = line.split(',')
				sec = int(float(params[0]))
				x = float(params[1])
				y = float(params[2])
				
				if not sec in times.keys():
					times[sec] = [[], []]
				times[sec][0].append(x)
				times[sec][1].append(y)

			elif re.match("^[0-9]+(\.[0-9]+)?\,-?[0-9]+(\.[0-9]+)?\,?$", line):
				params = line.split(',')
				sec = int(float(params[0]))
				x = float(params[1])
				
				if not sec in times.keys():
					times[sec] = []
				times[sec].append(x)
			else:
				writer.writerow(line.split(","))

		for key in times.keys():
			if isinstance(times[key], list) and not isinstance(times[key][0], list):
				#writer.writerow("%d,%s" % (key, str( ( sum(times[key]) / len(times[key]) ) ) ))
				writer.writerow([key, str( ( sum(times[key]) / len(times[key]) ) ) ])
			else:
				#writer.writerow("%d,%s,%s" % (key, str( ( sum(times[key][0]) / len(times[key][0]) ) ), str( ( sum(times[key][1]) / len(times[key][1]) ) )))
				writer.writerow([key, str( ( sum(times[key][0]) / len(times[key][0]) ) ), str( ( sum(times[key][1]) / len(times[key][1]) ) )])

def main():
    for file in only_files:
    	readpath = read_path + file
    	writepath = write_path + file
    	mutateCsv(readpath, writepath)
    print("Finished!")

if __name__ == '__main__':
	main()