import argparse
import sys

parser = argparse.ArgumentParser(description='Welcome to domainker help page')

parser.add_argument('-d','--domains',type=str, help='Domains File')
parser.add_argument('-i','--input',type=str, help='Single Host')
parser.add_argument('-o','--output',type=str, help='Output File')

parser.add_argument('-u','--url',action='store_true', help='Get Target Response Code With Some Additional Checks')
parser.add_argument('-F','--interesting-files',action='store_true', help='Check For Interesting Files, Requires [--url or --all]')

parser.add_argument('-P','--put',action='store_true', help='Check If [PUT] Method is Enabled')


parser.add_argument('-r','--spf',action='store_true', help='Check SPF Record')
parser.add_argument('-s','--struts',action='store_true', help='Attack Struts [CVE-2018-11776]')

parser.add_argument('-a','--aws',action='store_true', help='Check For Associated [AWS] Buckets')
parser.add_argument('-c','--crlf',action='store_true', help='Check For CRLF vulnerability')

parser.add_argument('-q','--dns',action='store_true', help='Get Target Cname')

parser.add_argument('-p','--cache-poisoning',action='store_true', help='Check For Cache Poisoning')

parser.add_argument('-A','--all',action='store_true', help='Run All Plugins [MEMORY HEAVY]')

parser.add_argument('-uu','--force-update',action='store_true', help='Force auto-update to run')
parser.add_argument('-t','--threads',type=int, help='Set Number Of Threads',default=10)
parser.add_argument('-rt','--request-timeout',type=int, help='Request Timeout',default=30)

args = parser.parse_args()
