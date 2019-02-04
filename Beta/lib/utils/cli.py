from __future__ import print_function
import colorama
import sys

colorama.init(autoreset=True)

def pprint(**kw):
	fmt = "\n[!] %s%s%s\n"% (colorama.Fore.LIGHTWHITE_EX,kw['HOST'],colorama.Fore.RESET)
	for key in kw:
		if kw[key] != None and key != 'HOST' and not str(key).startswith('__'):
			fmt += " |_> [{}]: {}\n".format(key,kw[key])
	fmt += "%s" % colorama.Fore.RESET

	print(fmt,end='')

def no_options():
	print('[ERR] Please choose a module')
	sys.exit(0)

def start_pause():
	raw_input(colorama.Fore.YELLOW + "[!] Press enter to start ")

def end_pause():
	raw_input("\n"+colorama.Fore.GREEN + "[!] Finished enter to exit ")


def info(args):
	print("[INFO]\n  |_> Number of thread(s): {}\n  |_> Thread(s) timeout: {}\n  |_> Request(s) timeout: {}\n".format(args.threads,args.thread_timeout,args.request_timeout))
