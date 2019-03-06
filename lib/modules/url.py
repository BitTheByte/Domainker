import requests
import colorama
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

headers_list = [
	"X-Frame-Options",
	"X-XSS-Protection",
	"X-Content-Type-Options"
]

def chkurl(url,check_headers,timeout=60):
	try:
		res = requests.get(url,timeout=timeout,verify=False)
		if str(res.status_code)[0] == "2": output= colorama.Fore.GREEN  + str(res.status_code)
		if str(res.status_code)[0] == "3": output= colorama.Fore.YELLOW + str(res.status_code)
		if str(res.status_code)[0] == "4": output= colorama.Fore.BLUE   + str(res.status_code)
		if str(res.status_code)[0] == "5": output= colorama.Fore.RED    + str(res.status_code)
		
		if check_headers:
			for header in headers_list:
				for request_h in res.headers:
					if request_h.lower() == header.lower():
						break
				else:
					output += "%s\n        |> [Missing header]> %s" % (colorama.Fore.WHITE,header)
 		return output

	except Exception as e:
		return colorama.Fore.RED + 'Unreachable'
