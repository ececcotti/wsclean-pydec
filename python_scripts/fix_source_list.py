import re

filedata = open('CygA.skymodel', 'r')
filedata_write = open('CygA_fixed.skymodel','w')

count = 0
for line in filedata:
	li = line.strip()
	if not li.startswith('#'):
		line_split = re.split(', ',line)
		line_split[0] = line_split[0] + '_' + str(count)
		count += 1
		nsplit = len(line_split)
		new_line = ''
		for i in range(nsplit):
			if i != nsplit-1: new_line += line_split[i] + ', '
			else: new_line += line_split[i]
	else: new_line = li + '\n'
	filedata_write.write(new_line)		

filedata.close()
filedata_write.close()
         
