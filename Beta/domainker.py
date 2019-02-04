from lib.utils.helpers import read_file
from lib.utils.multi import Threader
from lib.utils.helpers import uri
from lib.modules.url import ckurl
from lib.modules.aws import ckaws
from lib.modules.cname import chkcname
from lib.utils.args import args
from lib.utils import cli


thread = Threader(args.threads)

def main(host,timeout=30):
	cli.pprint(
		HOST= uri(host),
		URL = ckurl(uri(host)) if args.url else None,
		DNS = chkcname(host) if args.dns else None,
		AWS = ckaws(host) if args.aws else None,
	)

if not args.url == 1 and not args.aws == 1:
	cli.no_options()


cli.info(args)
cli.start_pause()
for host in read_file(args.domains): thread.put(main, [host])
thread.finish_all()
cli.end_pause()
