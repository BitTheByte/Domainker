from requests import get
from colorama import Fore

def update(current_version):
	try:
		remote_version = float(get("https://raw.githubusercontent.com/BitTheByte/Domainker/master/lib/version").content.strip())
		if remote_version > current_version:
			print(" %s[WARNING] %sYou are using an old version of this tool"%(Fore.RED,Fore.LIGHTWHITE_EX))
	except:
		pass

def read_file(path):
	try:
		with open(path,"r") as file:
			for line in file:
				yield line.strip()
	except Exception as e:
		print(e)

			
def uri(url):
	if url.startswith("."):
		url = url[1::]
	if not url.startswith('http://'):
		url =  ("http://" + url)
	elif not url.startswith('https://'):
		url = ("https://" + url)
	return (url)

def durl(url):
	url = url.replace("https://","")
	url = url.replace("http://","")
	#if url.endswith("/"):
	#	url = url[0:-1]
	if url.startswith("."):
		url =  url[1::]
	return url
