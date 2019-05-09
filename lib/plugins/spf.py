from linker import *


def chkspf(endpoint,timeout=30):
	content = requests.post('http://spf.myisp.ch/',timeout=timeout, data= {
	  	'host': helpers.urlify(endpoint)['HOST']
	}).content

	if "No SPF records found." in content:
		return "%sVulnerable [NO SPF RECORD]" % Fore.RED
	else:
		return "%sSafe [FOUND SPF RECORD]" % Fore.GREEN

