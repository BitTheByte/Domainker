from datetime import datetime
from threading import Lock
from colorama import Fore
from datetime import date
from requests import get
from glob import glob
from args import args
import hashlib
import re
import os

lock = Lock()

def tree(paths):
	structure = []
	for path in paths:
		for f in glob(path):
			structure.append(f.replace("\\","/"))
	return structure

def scheduled_update():
	today = date.today()
	
	if not os.path.isfile("lib/core/update.sync"):
		open("lib/core/update.sync","w").write(str(today))
		return 0
	
	last_check = datetime.strptime(open("lib/core/update.sync","r").read().strip(),'%Y-%m-%d').date()
	diff = (today - last_check).days

	if args.force_update:
		print(" %s[%s*%s]%s: Forced Update is Running" % (Fore.BLUE,Fore.RED,Fore.BLUE,Fore.RESET))
		open("lib/core/update.sync","w").write(str(today))
		return 1

	if  diff >= 5:
		print(" %s[%s*%s]%s: Scheduled Automatic Update is Running" % (Fore.BLUE,Fore.RED,Fore.BLUE,Fore.RESET))
		open("lib/core/update.sync","w").write(str(today))
		return 1
	return 0

def remote_version(current_version):
	try:
		remote_version = float(get("https://raw.githubusercontent.com/BitTheByte/Domainker/master/lib/version",verify=False).content.strip())
		if remote_version > current_version:
			print(" %s[WARNING] %sYou are using an old version of this tool [%s] a newer version is available [%s]"%(Fore.RED,Fore.LIGHTWHITE_EX,current_version,remote_version))
		if float(open("../version","r").read().strip()) < 1.76:
			print(""" %s[CRITICAL] %sYou will encounter an error message during launch
            Advisory: https://github.com/BitTheByte/Domainker/issues/4"""%(Fore.RED,Fore.LIGHTWHITE_EX))
	except:
		pass

def md5(content):
	return hashlib.md5(re.sub(r'\s+', '', content)).hexdigest()

def remote_sync(repo_path):
	global lock
	github_base = "https://raw.githubusercontent.com/BitTheByte/Domainker/master/%s"

	remote_code = get(github_base % repo_path).content.strip()
	local_code  = open(repo_path,"r").read().strip()

	with lock:
		if md5(remote_code) != md5(local_code):
			print("  |> [%sUPDATED%s]: %s" % (Fore.CYAN,Fore.RESET,repo_path))
			open(repo_path,"w").write(remote_code)
		else:
			print("  |> [%sUP-TO-DATE%s]: %s" % (Fore.GREEN,Fore.RESET,repo_path))

