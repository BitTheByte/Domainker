from datetime import datetime
from threading import Lock
from colorama import Fore
from datetime import date
from requests import get
from glob import glob
from .args import args
import hashlib
import json
import re
import os

def md5(content): return hashlib.md5(re.sub(r'\s+', '', content).encode('utf-8')).hexdigest()

def hash_local_files(remote_table):
	table = {}
	for filepath,remote_md5 in remote_table.items():
		if os.path.isfile(filepath):
			table[filepath] = md5(open(filepath,'r').read())
		else:
			table[filepath] = None
	return table

def github_file_content(path):
	for tries in range(5):
		try:
			conn = get('https://raw.githubusercontent.com/BitTheByte/Domainker/master/%s' % path)
			return conn.text.replace('\r\n',"\n")
		except:
			return 'ERR'

def remote_version(current_version):
	remote_table = json.loads(get('https://raw.githubusercontent.com/BitTheByte/Domainker/master/lib/remote.db').text.strip())
	local_table  = hash_local_files(remote_table)

	for filepath,remote_md5 in remote_table.items():
		if local_table[filepath] == None:
			filedata = github_file_content(filepath)
			if filedata != 'ERR':
				open(filepath,'w').write(filedata)
				print(" >> [%sCREATED%s]: %s" % (Fore.YELLOW,Fore.RESET,filepath))
		else:
			if local_table[filepath] != remote_md5:
				open(filepath,'w').write(github_file_content(filepath))
				print(" >> [%sUPDATED%s]: %s" % (Fore.CYAN,Fore.RESET,filepath))
