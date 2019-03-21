import requests
import colorama
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

headers_list = [
	"X-Frame-Options",
	"X-XSS-Protection"
]

dir_listing = [
	"Index of",
	'alt="[DIR]"'
]

def chkurl(url,check_headers,timeout=60):
	try:
		res = requests.get(url,timeout=timeout,verify=False)
		if str(res.status_code)[0] == "2": output = colorama.Fore.GREEN  + str(res.status_code)
		if str(res.status_code)[0] == "3": output = colorama.Fore.YELLOW + str(res.status_code)
		if str(res.status_code)[0] == "4": output = colorama.Fore.BLUE   + str(res.status_code)
		if str(res.status_code)[0] == "5": output = colorama.Fore.RED    + str(res.status_code)


		if res.status_code == 200 and 'http://' in res.url:
			output+= " %s-[OVER HTTP]%s" % (colorama.Fore.RED,colorama.Fore.RESET)
		else:
			if res.history:
				if 'http://' in res.history[-1].url:
					output+= " %s-[OVER HTTP]%s" % (colorama.Fore.RED,colorama.Fore.RESET)


		for t in dir_listing:
			if t in res.content:
				output += " %s-[DIRECTORY LISTING]%s" % (colorama.Fore.RED,colorama.Fore.RESET)
				break
		
		if check_headers:
			for header in headers_list:
				for request_h in res.headers:
					if request_h.lower() == header.lower():
						break
				else:
					output += "%s\n        |> [MISSING HEADER]> %s" % (colorama.Fore.WHITE,header)
 		return output

	except Exception as e:
		return colorama.Fore.RED + 'Unreachable'
