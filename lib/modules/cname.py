from dns import resolver

def chkcname(host):
	try:
		answers = resolver.query(host, 'CNAME')
		return ','.join([str(rdata.target) for rdata in answers])
	except:
		return "NaN"
