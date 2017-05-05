import sys
import os
import shutil
from dateutil.parser import parse

execution_date = parse(sys.argv[1])
tmp_path = '/tmp/singer-sync/' + execution_date.strftime("%Y-%m-%d") + '/'
print("Deleting " + tmp_path + "...", end='')
shutil.rmtree(tmp_path) #if directory, deletes entire directory recursively
print("done")