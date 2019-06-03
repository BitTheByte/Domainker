from lib.core.updater import *
from lib.core.helpers import *

from lib.core.multi import Threader
from lib.core.args import args
from lib.core import cli

from lib.plugins.experimental.cache_poisoning import chkpoisoning
from lib.plugins.cname import chkcname
from lib.plugins.struts import chkstruts
from lib.plugins.spf import chkspf
from lib.plugins.crlf import chkcrlf
from lib.plugins.url import chkurl
from lib.plugins.aws import chkaws
from lib.plugins.put import chkput


version = 1.75
modules = [
	args.url,
	args.aws,
	args.dns, 
	args.crlf,
	args.cache_poisoning,
	args.struts,
	args.spf,
	args.put,
	args.all
]
