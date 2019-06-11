from .linker import *

FLAG_OVER_HTTP    = 101
FLAG_DIR_LISTING  = 103
interesting_files = [f.strip() for f in open("lib/wordlist/interesting_files.txt","r").readlines()]

def is_available(url):
	response = fetch(url)
	if response.code == 200:
		return response
	return 0

@helpers.on_error(attr(url='',code='down',content='',headers=[],content_length=0),0)
def fetch(url,fast_mode=1,timeout=30):
	if fast_mode == 1:
		request = requests.head(url,timeout=timeout,allow_redirects=True,verify=False)
		if 'content-length' in request.headers:
			return attr(url= request.url, code= request.status_code, content_length= request.headers['content-length'])
		return fetch(url,fast_mode=2)

	if fast_mode == 2:
		request = requests.get(url,timeout=timeout,allow_redirects=True,verify=False)
		return attr(url= request.url, code= request.status_code, content_length= len(request.text))

	request = requests.get(url,timeout=timeout,verify=False)
	if request.history:
		return attr(url= request.history[-1].headers['location'],code= request.history[-1].status_code,headers= request.history[-1].headers,content= request.text,content_length= len(request.text))
	return attr(url= request.url,code= request.status_code,content= request.text,content_length= len(request.text))

def search_for_files(endpoint,files,threads=5):
	endpoint          = helpers.urlify(endpoint).as_dir
	base_response     = fetch(endpoint).content_length
	base_404_response = fetch(endpoint + "dummy_not_found").content_length
	threads_result    = helpers.run_on_threading(is_available,
                        [endpoint + file for file in files],
                        threads)

	found = []
	for result in threads_result:
		if result.ret and not result.ret.content_length in (base_response,base_404_response):
			"""
			TODO: FIX THIS
			This can be tricked by 30x redirects
			host.com/.git -> 302 -> another.com/home
			return value: another.com/home
			"""
			found.append(result.ret.url)
	return found

def additional_checks(request):
	flags = []
	if 'http://' in request.url:
		flags.append(FLAG_OVER_HTTP)
	if 'Index of' in request.content or 'alt="[DIR]"' in request.content:
		flags.append(FLAG_DIR_LISTING)
	return flags

def chkurl(url,files_search,timeout):
		request = fetch(helpers.urlify(url).as_file, fast_mode=0)
		flags   = additional_checks(request)

		if request.code         == "down": output = Fore.RED    + "DOWN"
		if str(request.code)[0] == "2": output = Fore.GREEN  + str(request.code)
		if str(request.code)[0] == "4": output = Fore.BLUE   + str(request.code)
		if str(request.code)[0] == "5": output = Fore.RED    + str(request.code)
		if str(request.code)[0] == "3":
			output = Fore.YELLOW + str(request.code)
			output += '%s -> %s%s' % (Fore.GREEN,Fore.LIGHTWHITE_EX,request.url)

		if FLAG_OVER_HTTP in flags:
			output += " %s-[OVER HTTP]%s" % (Fore.RED,Fore.RESET)

		if FLAG_DIR_LISTING in flags:
			output += " %s-[DIRECTORY LISTING]%s" % (Fore.RED,Fore.RESET)

		if files_search and request.code!='down':
			files   = search_for_files(url, interesting_files )
			for file in files:
				output += "%s\n        |> [INTERESTING FILE]> %s%s" % (Fore.GREEN,Fore.WHITE,file)
		return output
