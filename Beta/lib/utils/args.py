import argparse


parser = argparse.ArgumentParser(description='Welcome to domainker help page')

parser.add_argument('-d','--domains',type=str, help='Domains list')
parser.add_argument('-a','--aws',action='store_true', help='Perform aws scan')
parser.add_argument('-q','--dns',action='store_true', help='Perform dns scan')
parser.add_argument('-u','--url',action='store_true', help='Perform url scan')
parser.add_argument('-o','--output',type=str, help='Output file')
parser.add_argument('-t','--threads',type=int, help='Number of threads default=20',default=10)
parser.add_argument('-T','--thread-timeout',type=int, help='Threads timeout default=30',default=30)
parser.add_argument('-rt','--request-timeout',type=int, help='Request timeout default=30',default=30)

args = parser.parse_args()
