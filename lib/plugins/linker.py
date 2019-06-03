import sys
sys.path.append('lib/core')
from botocore.handlers import disable_signing
from botocore.config import Config
from urlparse import urlparse
from botocore import UNSIGNED
from random import randint
from colorama import Fore
from colorama import init
from dns import resolver
from io import StringIO
import requests
import helpers
import boto3

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

