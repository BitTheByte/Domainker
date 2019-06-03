from linker import *

interesting_files = [f.strip() for f in open("lib/wordlist/interesting_files.txt","r").readlines()]
FLAG_OVER_HTTP = 101
FLAG_DIR_LISTING = 103

def OK(url):
	if fetch(url)['code'] == 200: return True
	return False
		
def fetch(url,timeout=30):
	try:
		request = requests.get(url,timeout=timeout,verify=False)
		if request.history: 
			return {
				'url':  request.history[-1].headers['location'],
				'code': request.history[-1].status_code,
				'content': request.content,
				'headers': request.history[-1].headers
			}

		return {
			'url': request.url,
			'code': request.status_code,
			'content': request.content,
			'headers': request.headers
		}

	except:
		return {
			'url': "",
			'code': "down",
			'content': "",
			'headers': []
		}

def search_for_files(endpoint,files,threads=5):
	endpoint = helpers.urlify(endpoint)['URL_DIR']
	search = []
	found  = []
	
	for file in files: search.append( endpoint + file )
	values = helpers.run_on_threading(OK,search,threads)

	for value in values:
		if value['return'] == True:
			found.append(value['args'][0])
	return found


def additional_checks(request):
	flags = []

	if 'http://' in request['url']:
		flags.append(FLAG_OVER_HTTP)
		
	if 'Index of' in request['content'] or 'alt="[DIR]"' in request['content']:
		flags.append(FLAG_DIR_LISTING)

	return flags

def chkurl(url,files_search,timeout):
		request = fetch( helpers.urlify(url)['URL_FILE'] )
		flags   = additional_checks(request)

		if request['code'] == "down": output = Fore.RED    + "DOWN"
		if str(request['code'])[0] == "2": output = Fore.GREEN  + str(request['code'])
		if str(request['code'])[0] == "4": output = Fore.BLUE   + str(request['code'])
		if str(request['code'])[0] == "5": output = Fore.RED    + str(request['code'])
		if str(request['code'])[0] == "3":
			output = Fore.YELLOW + str(request['code'])
			output += '%s -> %s%s' % (Fore.GREEN,Fore.LIGHTWHITE_EX,request['url'])

		if FLAG_OVER_HTTP in flags:
			output += " %s-[OVER HTTP]%s" % (Fore.RED,Fore.RESET)

		if FLAG_DIR_LISTING in flags:
			output += " %s-[DIRECTORY LISTING]%s" % (Fore.RED,Fore.RESET)

		if files_search and request['code']!='down':
			files   = search_for_files(url, interesting_files )
			for file in files:
				output += "%s\n        |> [INTERESTING FILE]> %s%s" % (Fore.GREEN,Fore.WHITE,file)

		return output
