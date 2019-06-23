from lib import *

def scan(endpoint,timeout=30):
	if not endpoint.strip(): return
	cli.pprint(
		HOST   = urlify(endpoint).as_file,
		URL    = chkurl(endpoint,args.interesting_files,timeout)        if args.all or args.url else None,
		AWS    = chkaws(endpoint,timeout)                               if args.all or args.aws else None,
		DNS    = chkcname(endpoint)                                     if args.all or args.dns else None,
		PUT    = chkput(endpoint,timeout)                               if args.all or args.put else None,
		CRLF   = chkcrlf(endpoint,timeout)                              if args.all or args.crlf else None,
		STRUTS = chkstruts(endpoint,timeout)                            if args.all or args.struts else None,
		SPF    = chkspf(endpoint,timeout)                               if args.all or args.spf else None,
		PORTS  = chkports(urlify(endpoint).host,args.ports)             if args.all or args.ports else None,
		CACHE  = chkpoisoning(urlify(endpoint).as_file,timeout)         if args.all or args.cache_poisoning else None,
	)

cli.banner()

remote_version(version)

for module in modules: 
	if module: break
else:
	cli.no_options()


cli.info(args)

if args.input:
	"""
		[Using -i] Single input handling
	"""
	scan(args.input,args.request_timeout)

else:
	"""
		[Using -d] Multi input file read handling
	"""
	thread = Threader(args.threads)
	for host in read_file(args.domains): thread.put(scan, [host,args.request_timeout])
	thread.finish_all()


if args.output != None:
	"""
		[Using -o] Output Saving
	"""
	cli.save_log(args.output)
