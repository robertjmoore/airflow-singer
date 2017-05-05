import sys
import os
import gzip
from dateutil.parser import parse

execution_date = parse(sys.argv[1])
base_path = '/tmp/singer-sync/' + execution_date.strftime("%Y-%m-%d") + '/'
tables = ['account', 'lead', 'opportunity', 'recordtype', 'task', 'user']
for table in tables:
	tmp_path = base_path + table + '/'
	print("   Evaluating path " + tmp_path)
	if not os.path.exists(tmp_path):
		print("   Doesn't exist, skipping")
		continue
	for filename in os.listdir(tmp_path):
		print("   Evaluating " + filename)
		if filename[-3:] != ".gz":
			continue
		fullfile = tmp_path + filename
		print("   Decompressing " + fullfile + "...", end='')
		inF = gzip.open(fullfile, 'rb')
		outF = open(fullfile[:-3], 'wb') #remove the .gz for the end file name
		outF.write( inF.read() )
		inF.close()
		outF.close()
		print("done")