from lib.core import helpers
from lib.core.helpers import attr
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

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

try:
	from urllib.parse import urlparse
except:
	from urlparse import urlparse