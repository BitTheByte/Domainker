import requests
import colorama
import requests.packages.urllib3
from urlparse import urlparse
requests.packages.urllib3.disable_warnings()

interesting_files = [
	"/.git",
	"/.git/config",
	"/.svn",
	"/.svn/config"
	"/.DS_Store",
	"/.env",
	"/Dockerfile",
	"/composer.json",
	"/web.config",
]

headers_list = [
	"X-Frame-Options",
	"X-XSS-Protection"
]

dir_listing = [
	"Index of",
	'alt="[DIR]"'
]

def chkurl(url,check_headers,check_interesting_files,timeout=60):

	try:
		res = requests.get(url,timeout=timeout,verify=False)
		
		if res.history:
			last_url = res.history[-1].headers['location']
			output = '%s%i %s-> %s%s ' % (
					colorama.Fore.YELLOW,
					res.history[-1].status_code,
					colorama.Fore.GREEN,
					colorama.Fore.LIGHTWHITE_EX,
					last_url
				) 
		else:
			last_url = res.url
			if str(res.status_code)[0] == "2": output = colorama.Fore.GREEN  + str(res.status_code)
			if str(res.status_code)[0] == "3": output = colorama.Fore.YELLOW + str(res.status_code)
			if str(res.status_code)[0] == "4": output = colorama.Fore.BLUE   + str(res.status_code)
			if str(res.status_code)[0] == "5": output = colorama.Fore.RED    + str(res.status_code)


		if 'http://' in last_url:
			output += " %s-[OVER HTTP]%s" % (colorama.Fore.RED,colorama.Fore.RESET)

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

		if check_interesting_files:
			for interesting_file in interesting_files:

				res = requests.get(url + interesting_file,timeout=timeout,verify=False)

				if res.history:
					scanned = res.history[-1].headers['location']
				else:
					scanned = res.url

				if res.status_code == 200:
					if urlparse(url + interesting_file).netloc == urlparse(scanned).netloc:
						if interesting_file in urlparse(scanned).path:
							output += "%s\n        |> [INTERESTING DIRECTORY]> %s%s" % (colorama.Fore.GREEN,colorama.Fore.WHITE,res.url)


 		return output

	except Exception as e:
		return colorama.Fore.RED + 'Unreachable'
