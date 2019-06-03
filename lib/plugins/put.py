from linker import *

@helpers.on_error("Unreachable")
def chkput(endpoint,timeout=30):
	url = helpers.urlify(endpoint)['URL_DIR'] + "domainker_{}.html".format(randint(0,0xffffffff))
	code = requests.put(url,data="DOMAINKER",timeout=timeout).status_code
	if code == 201:
		return "%sVulnerable %s:: %s%s" % (Fore.GREEN,Fore.YELLOW,Fore.LIGHTWHITE_EX,url)
	else:
		return "%sNot Vulnerable" % (Fore.RED)

