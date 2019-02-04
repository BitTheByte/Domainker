#!/usr/bin/env python
from __future__ import print_function
import requests
import os
try:
	import queue
execpt:
	import Queue as queue
import threading
import sys
import colorama
import argparse
from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

try:
	input = raw_input
except:
	pass

save_file = []

class Threader:
	def __init__(self,pool_size=1):
		self.q = queue.Queue()
		self.pool_size = pool_size

	def __t(self):
		thread = self.q.get()
		thread.daemon=True
		thread.start()

	def __name(self):
		return "DOMAINKER_THRD"

	def __wait(self):
		while 1:
			running = threading.enumerate()
			remain = [x.name for x in running if self.__name() in x.name]
			if len(remain) == 0:
				break


	def on_waiting(self):
		return self.q.qsize()


	def pop(self):
		return self.q.queue.pop()

	def finish_all(self):
		for _ in xrange(self.q.qsize()): self.__t()
		self.__wait()


	def put(self,target,args):
		if self.q.qsize() < self.pool_size:
			self.q.put(threading.Thread(target=target,name=self.__name(),args=tuple(args)))

		if self.q.qsize() >= self.pool_size:
			for _ in xrange(self.q.qsize()): self.__t()
			self.__wait()

def fix_url(url):

	if url[0] == ".":
		url = url[1::]

	if 'http' not in url[0:3]:
		url = "http://" + url

	return url

def scan_aws(url,timeout):

	if not args.aws: return -999

	while 1:
		try:
			aws = requests.get("http://%s.s3.amazonaws.com" % url,timeout=timeout)
			if aws.status_code == 404: return 0
			return 1
		except:
			pass

def scan_url(url,timeout):

	try:
		code = str(requests.get(url,timeout=timeout,verify=False).status_code)
	except:
		code = "DOWN"

	return code


def show(url,code,color,isAws):

	if isAws == 1:
		save_file.append((code,"[{code}] {url} - {aws}".format(
			code=code,
			url=url,
			aws="http://%s.s3.amazonaws.com" % url
		)))

	else:
		save_file.append((code,"[{code}] http://{url}".format(
			code=code,
			url=url,
		)))

	output = "{c}[{code}] http://{url}".format(
		c=color,
		code=code,
		url=url
	)

	if isAws == 1:
		output += " {c0}{c1}-> {c2}{aws}\n".format(
			c0=colorama.Fore.GREEN,
			c1=colorama.Fore.YELLOW,
			c2=colorama.Fore.LIGHTWHITE_EX,
			aws="http://%s.s3.amazonaws.com" % url
		)
	else:
		output += "\n"

	print(output,end='')


def main(url,timeout):

	url_status 	= scan_url(fix_url(url),timeout)
	aws_status  = scan_aws(url,timeout)

	if url_status[0] == "2": show(url, url_status, colorama.Fore.GREEN, aws_status)
	if url_status[0] == "3": show(url, url_status, colorama.Fore.YELLOW, aws_status)
	if url_status[0] == "4": show(url, url_status, colorama.Fore.BLUE, aws_status)
	if url_status[0] == "5": show(url, url_status, colorama.Fore.RED, aws_status)
	if url_status[0] == "D": show(url, url_status, colorama.Fore.RED, aws_status)




colorama.init(autoreset=True)
print (colorama.Fore.LIGHTBLACK_EX  + " ______   _______  __   __  _______  ___   __    _  ___   _  _______  ______   ")
print (colorama.Fore.LIGHTWHITE_EX  + "|      | |       ||  |_|  ||   _   ||   | |  |  | ||   | | ||       ||    _ |  ")
print (colorama.Fore.LIGHTBLACK_EX  + "|  _    ||   _   ||       ||  |_|  ||   | |   |_| ||   |_| ||    ___||   | ||  ")
print (colorama.Fore.LIGHTWHITE_EX  + "| | |   ||  | |  ||       ||       ||   | |       ||      _||   |___ |   |_||_ ")
print (colorama.Fore.LIGHTBLACK_EX  + "| |_|   ||  |_|  ||       ||       ||   | |  _    ||     |_ |    ___||    __  |")
print (colorama.Fore.LIGHTWHITE_EX  + "|       ||       || ||_|| ||   _   ||   | | | |   ||    _  ||   |___ |   |  | |")
print (colorama.Fore.LIGHTBLACK_EX  + "|______| |_______||_|   |_||__| |__||___| |_|  |__||___| |_||_______||___|  |_|\n")



parser = argparse.ArgumentParser(description='Welcome to domainker help page')

parser.add_argument('-d','--domains'		,type=str, help='Domains list')
parser.add_argument('-a','--aws'		,action='store_true', help='Perform aws checking')
parser.add_argument('-o','--output'		,type=str, help='Output file')
parser.add_argument('-t','--threads'		,type=int, help='Number of threads default=20',default=10)
parser.add_argument('-T','--thread-timeout'	,type=int, help='Threads timeout default=30',default=30)
parser.add_argument('-rt','--request-timeout'	,type=int, help='Request timeout default=30',default=30)

args = parser.parse_args()

if  args.domains == None:
	print (colorama.Fore.RED + "[!] Please select the domains file using -d argument")
	sys.exit()


print(colorama.Fore.YELLOW + "[INFO]\n  |_> Number of thread(s): {}\n  |_> Thread(s) timeout: {}\n  |_> Request(s) timeout: {}\n".format(args.threads,args.thread_timeout,args.request_timeout))
input(colorama.Fore.CYAN + "[R] Press enter to start\n")

threader = Threader(args.threads)

for _,url in enumerate(open(args.domains,"r").readlines()):
	threader.put(main,[url.strip(),args.request_timeout])
threader.finish_all()

if args.output is not None:
	for _,line in sorted(save_file):
		open(args.output ,"a").write(line + "\n")


input("\n"+colorama.Fore.YELLOW + "[*] Finished ..  Enter to exit")
