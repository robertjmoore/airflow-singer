import sys
import os
import json
from dateutil.parser import parse
import ntpath

execution_date = parse(sys.argv[1])
tmp_path = '/tmp/singer-sync/' + execution_date.strftime("%Y-%m-%d") + '/'
tables = ['account', 'lead', 'opportunity', 'recordtype', 'task', 'user']
config = { "files":	[] }
for table in tables:
	entry = {	"entity" : table,
			"file" : tmp_path + table + '/',
			"keys" : ["Id"]
					}
	config["files"].append(entry)

s = json.dumps(config)
file_path = tmp_path + "csv-config.json"
json_file = open(file_path, "w")
json_file.write(s)
json_file.close()
print("Wrote singer config file to " + file_path)