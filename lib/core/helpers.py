from requests import get
from colorama import Fore
from multi import Threader
from urlparse import urlparse


def run_on_threading(function,arguments,threads=5):
	stored_values = []
	def wrap(function,*args):
		ret = function(*args)
		stored_values.append( {'args':args,'return':ret} )

	threader = Threader(threads)
	for arg in arguments:
		threader.put(wrap, [function,arg] )

	threader.finish_all()
	return stored_values


def urlify(var):
	parts = urlparse(var)._asdict()
	if not parts['scheme'] and not parts['netloc']:
		parts['netloc'],parts['path'] = parts['path'],parts['netloc']

	if not parts['scheme']: parts['scheme'] = "http"

	URL = "%s://%s%s" % (parts['scheme'],parts['netloc'],parts['path'])
	  

	URL_FILE = URL if URL[-1]!="/" else URL [0:-1]
	URL_DIR  = URL if URL[-1]=="/" else URL + "/"

	return {
		'HOST': parts['netloc'],
		'URL_FILE': URL_FILE ,
		'URL_DIR' : URL_DIR
	}



def update(current_version):
	try:
		remote_version = float(get("https://raw.githubusercontent.com/BitTheByte/Domainker/master/lib/version",verify=False).content.strip())
		if remote_version > current_version:
			print(" %s[WARNING] %sYou are using an old version of this tool [%s] a newer version is available [%s]"%(Fore.RED,Fore.LIGHTWHITE_EX,current_version,remote_version))
	except:
		pass


def read_file(path):
	try:
		with open(path,"r") as file:
			for line in file:
				yield line.strip()
	except Exception as e:
		print(e)