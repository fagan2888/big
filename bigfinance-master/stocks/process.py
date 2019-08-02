import sys,os

for filename in os.listdir('./'):
	if 'txt' not in filename:
		continue
	f = open(filename, 'r', encoding='gbk')
	lines = f.readlines()
	f.close()
	f = open(filename, 'w', encoding='utf-8')
	for line in lines:
		if ('SZ' not in line) and ('SH' not in line):
			continue
		f.write(line)

	f.close()