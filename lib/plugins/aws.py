from .linker import *

upload_name = 'domainker_aws_poc.html'
upload_body = "<html><!-- DOMAINKER_TAKEOVER(This is a vulnerable host) --></html>"

@helpers.on_error("Access Denied")
def tkaws(bucket):
	s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
	try:
		s3.put_object(Bucket=bucket, Key=upload_name,ACL='public-read', Body=StringIO(unicode(upload_body)).read())
	except:
		s3.put_object(Bucket=bucket, Key=upload_name,ACL='public-read', Body=StringIO(str(upload_body)).read())
	response = requests.get("http://{bucket}.s3.amazonaws.com/{target}".format(bucket=bucket,target=upload_name)).text
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


@helpers.on_error("Access Denied")
def chkacl(bucket):
	allUsersGrants = []
	s3 = boto3.resource('s3')
	s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
	bucket_acl = s3.BucketAcl(bucket.encode('utf8'))
	bucket_acl.load()

	for grant in bucket_acl.grants:
		if 'URI' in grant['Grantee']:
			if grant['Grantee']['URI'] == "http://acs.amazonaws.com/groups/global/AllUsers":
				allUsersGrants.append(grant['Permission'])	
	ret = ""			
	for p in allUsersGrants:
		ret += "%s%s%s," % (Fore.LIGHTCYAN_EX,p,Fore.RESET)
	ret = ret[:-1]
	return ret

@helpers.on_error(0,0)
def fakesig(endpoint,timeout):
	params = {"AWSAccessKeyId":"AKIAI4UZT4FCOF2OTJYQ","Expires":"1766972005","Signature":"domainker"}
	result = requests.get("http://{}/dummy".format(endpoint),params=params,timeout=timeout)
	if result.status_code == 403 and "AWSAccessKeyId" in result.content:
		bucket = re.findall("/.+/dummy",result.content)[0]
		bucket = bucket.replace("/dummy","")
		return bucket[1::]
	else:
		return 0

@helpers.on_error(0,0)
def gets3(endpoint,timeout):
	aws = requests.get("http://%s.s3.amazonaws.com" % endpoint,timeout=timeout)
	if aws.status_code == 404:
		return 0
	return endpoint

@helpers.on_error("Unreachable")
def chkaws(endpoint,timeout):
	bucket = helpers.urlify(endpoint).host
	
	method1 = fakesig(bucket,timeout)
	method2 = 0
	if not method1:
		method2 = gets3(bucket,timeout)

	if method1 == 0 and method2 == 0:
		return '%sNo [AWS] Bucket Associated With The Endpoint' % (Fore.RED)

	bucket = [i for i in [method1,method2] if i][0]

	msg = '%sFound [AWS] Bucket %s::%s ' "http://%s.s3.amazonaws.com%s" % (Fore.GREEN,Fore.YELLOW,Fore.LIGHTWHITE_EX,bucket,Fore.RESET)
	msg += '\n        |> Upload Result [%s]' % tkaws(bucket)
	msg += '\n        |> Acl Result [%s]' % chkacl(bucket)

	aws = requests.get("http://%s.s3.amazonaws.com" % endpoint)
	if '<Name>' in aws.text or 'ListBucketResult' in aws.text:
		msg += '\n        |> File(s) Listing [%sEnabled%s]' % (Fore.GREEN,Fore.RESET)
	else:
		msg += '\n        |> File(s) Listing [%sDisabled%s]' % (Fore.RED,Fore.RESET)
	return msg

