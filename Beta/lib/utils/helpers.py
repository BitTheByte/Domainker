

def read_file(path):
	with open(path,"r") as file:
		for line in file:
			yield line.strip()
			
def uri(url):
	if not url.startswith('http://'):
		return ("http://" + url)

	if not url.startswith('https://'):
		return ("https://" + url)
