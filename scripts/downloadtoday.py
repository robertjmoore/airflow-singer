import sys
import boto3
import os
from dateutil.parser import parse
import ntpath

execution_date = parse(sys.argv[1])
base_path = '/tmp/singer-sync/' + execution_date.strftime("%Y-%m-%d") + '/'
if not os.path.exists(base_path):
	print("   creating base directory " + base_path)
	os.makedirs(base_path)

bucketname = 'my-bucket'
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)
tables = ['account', 'lead', 'opportunity', 'recordtype', 'task', 'user']
for table in tables:
	tmp_path = base_path + table + '/'
	prefix = 'source/sfdc/' + table + '/incr/year=' + str(execution_date.year) + '/month=' + str('{:02d}'.format(execution_date.month)) + '/day=' + str('{:02d}'.format(execution_date.day)) + '/'
	print("searching prefix: " + prefix)
	for obj in bucket.objects.filter(Prefix=prefix):
		print("Found " + bucket.name + ": " + obj.key)
		if not os.path.exists(tmp_path):
			print("   creating directory " + tmp_path)
			os.makedirs(tmp_path)
		localfile = tmp_path + ntpath.basename(obj.key)
		print("   Downloading to " + localfile + "...", end='')
		s3.meta.client.download_file(bucket.name, obj.key, localfile)
		print("done")
