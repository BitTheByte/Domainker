import requests
import os
import threading
import random
import glob
import sys
import colorama
import argparse

from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



storeThreads = []
def threadManager(function,Funcargs,Startthreshold,Threadtimeout=5):
	if len(storeThreads) != Startthreshold:
		storeThreads.append(threading.Thread(target=function,args=tuple(Funcargs) ))
	if len(storeThreads) == Startthreshold:
		for metaThread in storeThreads:
			metaThread.start()
		for metaThread in storeThreads:
			metaThread.join(Threadtimeout)
		del storeThreads[::]


R2XX = []
R3XX = []
R4XX = []
R5XX = []
DOWN = []


def CheckURL(URL,timeout):

	if URL[0] == ".":
		URL = URL[1::]


	if 'http' not in URL[0:3]:
		URL = "http://" + URL 

	try:
		CODE = str(requests.get(URL,timeout=timeout,verify=False).status_code)
	except:
		CODE = "down"


	if CODE[0] == "2":
		R2XX.append(URL)
		print colorama.Fore.GREEN  + "[2XX] {0}\n".format(URL),
	if CODE[0] == "3":
		R3XX.append(URL)
		print colorama.Fore.YELLOW + "[3XX] {0}\n".format(URL),
	if CODE[0] == "4":
		R4XX.append(URL)
		print colorama.Fore.BLUE   + "[4XX] {0}\n".format(URL),
	if CODE[0] == "5":
		R5XX.append(URL)
		print colorama.Fore.CYAN   + "[5XX] {0}\n".format(URL),
	if CODE == "down":
		DOWN.append(URL)
		print colorama.Fore.RED    + "[DOWN] {0}\n".format(URL),




colorama.init(autoreset=True)






print colorama.Fore.YELLOW  + " ______   _______  __   __  _______  ___   __    _  ___   _  _______  ______   "
print colorama.Fore.YELLOW  + "|      | |       ||  |_|  ||   _   ||   | |  |  | ||   | | ||       ||    _ |  "
print colorama.Fore.RED     + "|  _    ||   _   ||       ||  |_|  ||   | |   |_| ||   |_| ||    ___||   | ||  "
print colorama.Fore.RED     + "| | |   ||  | |  ||       ||       ||   | |       ||      _||   |___ |   |_||_ "
print colorama.Fore.RED     + "| |_|   ||  |_|  ||       ||       ||   | |  _    ||     |_ |    ___||    __  |"
print colorama.Fore.YELLOW  + "|       ||       || ||_|| ||   _   ||   | | | |   ||    _  ||   |___ |   |  | |"
print colorama.Fore.YELLOW  + "|______| |_______||_|   |_||__| |__||___| |_|  |__||___| |_||_______||___|  |_|"
print ""







parser = argparse.ArgumentParser(description='Welcome to domainker help page')
parser.add_argument('-d', type=str, help='Domains list')
parser.add_argument('-o', type=str, help='Output file')
parser.add_argument('-t', type=int, help='Number of threads default=10')
parser.add_argument('-T', type=int, help='Threads timeout default=60')
parser.add_argument('-rt',type=int, help='Request timeout default=30')

args = parser.parse_args()

if  args.d == None:
	print colorama.Fore.RED + "[!] Please select the domains file using -d argument"
	sys.exit()



LinksFile		= open(args.d,"r").readlines()
NumberOfThreads = args.t
ThreadTimeOut 	= args.T
RequestTimeOut  = args.rt



if NumberOfThreads is None:
	NumberOfThreads = 10

if ThreadTimeOut is None:
	ThreadTimeOut   = 5

if RequestTimeOut is None:
	RequestTimeOut  = 4


print colorama.Fore.YELLOW + "[INFO]\n  |_> Number of thread(s): {}\n  |_> Thread(s) timeout: {}\n  |_> Request(s) timeout: {}\n\n".format(NumberOfThreads,ThreadTimeOut,RequestTimeOut)
raw_input(colorama.Fore.CYAN + "[R] Press enter to start")




for Index,URL in enumerate(LinksFile):

	URL = URL.strip()

	if (len(LinksFile)-Index) < NumberOfThreads:

		threadManager(CheckURL,[URL,RequestTimeOut], (len(LinksFile)-Index)+1,ThreadTimeOut)

	else:

		threadManager(CheckURL,[URL,RequestTimeOut], NumberOfThreads,ThreadTimeOut)





if args.o is not None:
	#print colorama.Fore.GREEN + "[-] Saving to file"
	for R in R2XX:
		open(args.o,"a+").write("[2XX] %s\n" % R)
	for R in R3XX:
		open(args.o,"a+").write("[3XX] %s\n" % R)
	for R in R4XX:
		open(args.o,"a+").write("[4XX] %s\n" % R)
	for R in R5XX:
		open(args.o,"a+").write("[5XX] %s\n" % R)
	for R in DOWN:
		open(args.o,"a+").write("[DOWN] %s\n" % R)

raw_input(colorama.Fore.YELLOW + "[*] Finished .. press enter to exit")