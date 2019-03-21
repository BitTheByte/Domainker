import argparse

parser = argparse.ArgumentParser(description='Welcome to domainker help page')

parser.add_argument('-d','--domains',type=str, help='Domains file')
parser.add_argument('-i','--input',type=str, help='Single host')
parser.add_argument('-o','--output',type=str, help='Output file')

parser.add_argument('-H','--headers',action='store_true', help='Check for missing security headers')
parser.add_argument('-a','--aws',action='store_true', help='Check if target is hosted on Amazon aws')
parser.add_argument('-c','--crlf',action='store_true', help='Check for CRLF vulnerability')
parser.add_argument('-q','--dns',action='store_true', help='Get target cname')
parser.add_argument('-p','--cache-poisoning',action='store_true', help='Check for cache poisoning')
parser.add_argument('-u','--url',action='store_true', help='Get target response code and some additional checks')
parser.add_argument('-x','--aws-takeover',action='store_true', help='Takeover aws')


parser.add_argument('-t','--threads',type=int, help='Number of threads default=20',default=10)
parser.add_argument('-T','--thread-timeout',type=int, help='Threads timeout default=30',default=30)
parser.add_argument('-rt','--request-timeout',type=int, help='Request timeout default=30',default=30)

args = parser.parse_args()
