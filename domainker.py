from lib.utils.helpers import read_file
from lib.utils.helpers import update
from lib.utils.helpers import durl
from lib.utils.helpers import uri

from lib.utils.multi import Threader
from lib.utils.args import args
from lib.utils import cli

from lib.modules.experimental.cache_poisoning import chkpoisoning
from lib.modules.cname import chkcname
from lib.modules.crlf import chkcrlf
from lib.modules.url import chkurl
from lib.modules.aws import chkaws


__VERSION__ = 1.2
modules = [
	args.url,
	args.aws,
	args.dns, 
	args.crlf,
	args.cache_poisoning
]

def URL(host): return uri(durl(host))

def main(host,timeout=30):
	if not host.strip(): return
	cli.pprint(
		HOST  = URL(host),
		URL   = chkurl(URL(host),args.headers,timeout) if args.url else None,
		DNS   = chkcname(durl(host)) if args.dns else None,
		AWS   = chkaws(durl(host),args.aws_takeover,timeout) if args.aws else None,
		CRLF  = chkcrlf(URL(host),timeout) if args.crlf else None,
		CACHE = chkpoisoning(URL(host),timeout) if args.cache_poisoning else None
	)



cli.banner()
update(__VERSION__)

for module in modules:
	if module: break
else: cli.no_options()

cli.info(args)

if args.input: main(args.input,args.request_timeout)
else:
	thread = Threader(args.threads)
	for host in read_file(args.domains): thread.put(main, [host,args.request_timeout])
	thread.finish_all()

if args.output != None: cli.save_log(args.output)
