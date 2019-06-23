"""
FOR DEVELOPERS ONLY
PYTHON BUILDER FOR REMOTE.DB FILE
"""
import hashlib
import json
import re
import os

def md5(content): return hashlib.md5(re.sub(r'\s+', '', content).encode('utf-8')).hexdigest()
files = [ os.path.join(parent, name) for (parent, subdirs, files) in os.walk('.') for name in files + subdirs ]
table = {}
for name in files:
	for bad in [os.path.basename(__file__),'.txt','.md','.pyc','.git','.png','.db']:
		if bad in name:break
	else:
		name = name.replace('.\\','').replace('\\','/')
		if '.' in name: table.update({name:md5(open(name,"r").read())})
open("lib/remote.db","w").write(json.dumps(table))
