#!/usr/bin/python

import os

def read_csv(filename,delimeter:str) -> list:
	table = []
	if os.path.exists(filename):

		
		with open(filename) as file:
			for line in file:
				lst_line = []
				quote = 0
				for i in line:
					# Treat lines by symbols
					if i == delimeter:
						if quote:
						# if we open quote ", we add delimeter symbol, not whitespace  
							lst_line.append(delimeter)
						else:
					# substitute delimeter by spaces
							lst_line.append(' ')

					elif i == '"':
					# opening and closing of quotes
						quote = (quote + 1) % 2
					else:
					# If i is not delimeter or quote, we just append it
						lst_line.append(i)
				# join and split by spaces the result string and add result list in 'table' 
				table.append(''.join(lst_line).split())
	else:
		print("Error, such file doesn't exist")

# P.S. I suppose throw of exception instead printing is better approach
	
	return table 




def write_csv(filename,data,delimeter:str):

# What is incorrect call for write_csv?

	with open(filename,'w') as file:
		for row in data:
			file.write(delimeter.join(row)+"\n")



