from lib.utils.helpers import read_file
from lib.utils.helpers import durl
from lib.utils.helpers import uri

from lib.utils.multi import Threader
from lib.utils.args import args
from lib.utils import cli

from lib.modules.cname import chkcname
from lib.modules.crlf import chkcrlf
from lib.modules.url import chkurl
from lib.modules.aws import chkaws




modules = [
	args.url,
	args.aws,
	args.dns, 
	args.crlf
]


thread = Threader(args.threads)

def main(host,timeout=30):
	if not host.strip(): return

	cli.pprint(
		HOST = uri(durl(host)),
		URL  = chkurl(uri(durl(host)),timeout) if args.url else None,
		DNS  = chkcname(durl(host)) if args.dns else None,
		AWS  = chkaws(durl(host),args.aws_takeover,timeout) if args.aws else None,
		CRLF = chkcrlf(uri(durl(host)),timeout) if args.crlf else None
	)


		
cli.banner()

for module in modules:
	if module: break
else:
	cli.no_options()

cli.info(args)

for host in read_file(args.domains): thread.put(main, [host])
thread.finish_all()

if args.output != None: cli.save_log(args.output)
