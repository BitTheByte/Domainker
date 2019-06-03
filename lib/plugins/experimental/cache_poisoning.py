import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from colorama import Fore

# TEST
forwarded_host = "bitthebyte.com"

def chkpoisoning(host,timeout):
	try:
		request = requests.get(host,headers={
				'X-Forwarded-Host':forwarded_host,
				#'X-Host':forwarded_host,
				#'Host':forwarded_host
			},verify=False,timeout=timeout)

		if forwarded_host in request.content:
			return "%sMaybe Vulnerable - [X-Forwarded-Host] Reflected at Response" % (Fore.GREEN)

		if request.history:
			for request in request.history:
				if "Location" in request.headers:
					if forwarded_host in request.headers["Location"]:
						return "%sMaybe vulnerable - [X-Forwarded-Host] Reflected at Headers" % (Fore.GREEN)
		return "%sNot Vulnerable" % Fore.RED
	except Exception as e:
		return "%sUnreachable" % Fore.RED
