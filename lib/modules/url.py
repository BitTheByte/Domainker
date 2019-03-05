import requests
import colorama
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def chkurl(url,timeout=60):
	try:
		res = str(requests.get(url,timeout=timeout,verify=False).status_code)

		if res[0] == "2": return colorama.Fore.GREEN  + res
		if res[0] == "3": return colorama.Fore.YELLOW + res 
		if res[0] == "4": return colorama.Fore.BLUE   + res 
		if res[0] == "5": return colorama.Fore.RED    + res
 

	except:
		return colorama.Fore.RED + 'Unreachable'
