from lib.core.multi import Threader
from lib.core.args import args
from colorama import Fore
try:
	from urllib.parse import urlparse
except:
	from urlparse import urlparse

def attr(**kwargs):
	class cls(object):
		pass
	instance = cls()
	for key,value in list(kwargs.items()):
		setattr(instance, key, value)
	return instance

def on_error(error_msg,color=1):
	def decorator(function):
		def wrapper(*args, **kwargs):
			try:
				result = function(*args, **kwargs)
				return result
			except Exception as e:
				# print(e) For testing only
				if color:
					return "%s%s%s" %(Fore.RED,error_msg,Fore.RESET)
				return error_msg
		return wrapper
	return decorator

def run_on_threading(function,arguments,threads=5):
	stored_values = []
	def wrap(function,*args):
		ret = function(*args)
		stored_values.append( attr(args =args, ret=ret) )
		return 0

	threader = Threader(threads,name='run_on_threading')
	for arg in arguments:
		threader.put(wrap, [function,arg] )

	threader.finish_all()
	return stored_values

def urlify(var):
	parts = urlparse(var)._asdict()
	if args.https: parts['scheme'] = "https"

	if not parts['scheme'] and not parts['netloc']:
		parts['netloc'],parts['path'] = parts['path'],parts['netloc']

	if not parts['scheme']: parts['scheme'] = "http"

	URL = "%s://%s%s" % (parts['scheme'],parts['netloc'],parts['path'])

	return attr(host = parts['netloc'],
			as_file  = URL if URL[-1]!="/" else URL [0:-1],
			as_dir   = URL if URL[-1]=="/" else URL + "/")


def read_file(path):
	try:
		with open(path,"r") as file:
			for line in file:
				yield line.strip()
	except Exception as e:
		print(e)
