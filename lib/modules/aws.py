import requests
import colorama 

from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def ckaws(url,timeout=60):
	try:
		aws = requests.get("http://%s.s3.amazonaws.com" % url,timeout=timeout)
		if aws.status_code == 404:
			return '%sNot hosted on AWS' % colorama.Fore.RED
		
		return '%sHosted on AWS %s-> %s%s' % (colorama.Fore.GREEN,colorama.Fore.YELLOW,colorama.Fore.LIGHTWHITE_EX,"http://%s.s3.amazonaws.com" % url)

	except:
		pass
