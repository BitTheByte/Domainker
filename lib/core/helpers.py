from colorama import Fore
from multi import Threader
from urlparse import urlparse

def on_error(error_msg):
	def decorator(function):
		def wrapper(*args, **kwargs):
			try:
				result = function(*args, **kwargs)
				return result
			except Exception as e:
				return "%s%s%s" %(Fore.RED,error_msg,Fore.RESET)
		return wrapper
	return decorator

def run_on_threading(function,arguments,threads=5):
	stored_values = []
	def wrap(function,*args):
		ret = function(*args)
		stored_values.append( {'args':args,'return':ret} )
		return 0

	threader = Threader(threads,name='run_on_threading')
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


def read_file(path):
	try:
		with open(path,"r") as file:
			for line in file:
				yield line.strip()
	except Exception as e:
		print(e)
