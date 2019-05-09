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
	
	fmt = "\n %s[%s*%s] %s%s%s%s\n"% (
		colorama.Fore.BLUE, colorama.Fore.LIGHTRED_EX,colorama.Fore.BLUE,colorama.Fore.RESET
		,colorama.Fore.LIGHTWHITE_EX,kw['HOST'],colorama.Fore.RESET)
	for key in kw:
		if kw[key] != None and key != 'HOST' and not str(key).startswith('__'):
			fmt += "  |_> [{}]: {}{}\n".format(key,kw[key],colorama.Fore.RESET)

	with lock:
		log += fmt
		print(fmt,end='')

def no_options():
	print(' [ERR] Please choose a module')
	sys.exit(0)

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def save_log(path):
	open(path,"w").write(escape_ansi(log))


def info(args):
	print(" [INFO]\n  |_> Number of thread(s): {}\n  |_> Request(s) timeout: {}\n".format(args.threads,args.request_timeout))


def banner():
	print("""
  {G} ______{r}                    {R}_{r}      {Y} _                         
  {G}(______){r}                  {R}(_){r}     {Y}| |                     
  {G} _     _ {r}{Y} ___  ____  _____ _ ____ | |  _ _____  ____           
  {G}| |   | /{r}{Y}/ _ \|    \(____ | |  _ \| |_/ ) ___ |/ ___)        
  {G}| |__/ /{r}{Y}/ |_| | | | / ___ | | | | |  _ (| ____| |           
  {G}|_____/{r}{Y} \____/|_|_|_\_____|_|_| |_|_| \_)_____)_|{r}
  """.format(
			R=colorama.Fore.LIGHTRED_EX,
			r=colorama.Fore.RESET,
			G=colorama.Fore.LIGHTGREEN_EX,
			Y=colorama.Fore.YELLOW
			))
	print (colorama.Fore.LIGHTBLUE_EX + "      > [ Github ] https://github.com/BitTheByte/Domainker\n")
