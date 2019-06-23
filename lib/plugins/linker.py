from lib.core import helpers
from lib.core.helpers import attr
from lib.core.multi import Threader
from lib.core.args import args
from botocore.handlers import disable_signing
from botocore.config import Config
from botocore import UNSIGNED
from random import randint
from colorama import Fore
from colorama import init
from dns import resolver
from io import StringIO
import requests
import boto3
import socket
import threading

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

try:
	from urllib.parse import urlparse
except:
	from urlparse import urlparse