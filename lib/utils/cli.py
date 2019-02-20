from __future__ import print_function
from threading import Lock
import colorama
import re
import sys

log = ""
lock = Lock()
colorama.init(autoreset=True)

def pprint(**kw):
	global log

	fmt = "\n[!] %s%s%s\n"% (colorama.Fore.LIGHTWHITE_EX,kw['HOST'],colorama.Fore.RESET)
	for key in kw:
		if kw[key] != None and key != 'HOST' and not str(key).startswith('__'):
			fmt += " |_> [{}]: {}\n".format(key,kw[key])
	fmt += "%s" % colorama.Fore.RESET

	with lock:
		log += fmt
	print(fmt,end='')

def no_options():
	print('[ERR] Please choose a module')
	sys.exit(0)

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def save_log(path):
	open(path,"w").write(escape_ansi(log))

def start_pause():
	raw_input(colorama.Fore.YELLOW + "[!] Press enter to start ")

def end_pause():
	raw_input("\n"+colorama.Fore.GREEN + "[!] Finished enter to exit ")


def info(args):
	print("[INFO]\n  |_> Number of thread(s): {}\n  |_> Thread(s) timeout: {}\n  |_> Request(s) timeout: {}\n".format(args.threads,args.thread_timeout,args.request_timeout))
