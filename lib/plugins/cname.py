from linker import *

@helpers.on_error("NaN")
def chkcname(endpoint):
	answers = resolver.query(helpers.urlify(endpoint)['HOST'], 'CNAME')
	return ','.join([str(rdata.target) for rdata in answers])

