from linker import *

def chkcname(endpoint):
	try:
		answers = resolver.query(helpers.urlify(endpoint)['HOST'], 'CNAME')
		return ','.join([str(rdata.target) for rdata in answers])
	except:
		return "NaN"
