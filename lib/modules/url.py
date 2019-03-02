import requests
import colorama
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def ckurl(url,timeout=60):
	try:
		res = str(requests.get(url,timeout=timeout,verify=False).status_code)

		if res[0] == "2": return colorama.Fore.GREEN  + res + colorama.Fore.RESET     
		if res[0] == "3": return colorama.Fore.YELLOW + res + colorama.Fore.RESET      
		if res[0] == "4": return colorama.Fore.BLUE   + res + colorama.Fore.RESET      
		if res[0] == "5": return colorama.Fore.RED    + res + colorama.Fore.RESET     
 

	except:
		return colorama.Fore.RED + 'Down' + colorama.Fore.RESET     
