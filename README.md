# Domainker (Beta)
![](https://raw.githubusercontent.com/BitTheByte/Domainker/master/lib/banner.png "Logo Title Text 1")
# Setup
- Python pip
```
pip install domainker
```
- Manual setup 
```
git clone https://github.com/BitTheByte/Domainker
cd Domainker
python setup.py install
```
 
 
# How to use
I developed this tool to be easily managed and upgraded so i created it as small plugin systems connected together

## Plugins and usage
```
lib\modules\experimental\cache_poisoning.py : [--cache-poisoning] Check if the host is vulnerable to cache poisoning
lib\modules\crlf.py   : [--crlf] Check if host is vulnerable to CRLF
lib\modules\aws.py    : [--aws] Check if target is hosted on amazon (Use -x to run Auto-Takeover)
lib\modules\cname.py  : [--dns] Return host cname
lib\modules\url.py    : [--url] Return host response code [See the options for more details]
lib\modules\struts.py : [--struts] Perform struts attack
lib\modules\spf.py    : [--spf] Check for spf record
```

## Basic usage
 ```
 $ domainker -i google.com [.. Plugins]
 $ domainker -d mydomains_list.txt [.. Plugins]
 $ domainker -d mydomains_list.txt --url
 $ domainker -d mydomains_list.txt --dns
 ```
You could also use multiple plugins at the same time
```
$ domainker -d mydomains_list.txt --url --dns --aws ...
$ domainker -i google.com --url --dns --aws ...
```
## Options
```
$ domainker --help
```
- Create output file [--output/-o file_name]
- Threads count [--threads/-t number]
- Takeover aws [--aws-takeover/-x] [--aws required]
- Missing headers [--headers/-H] [--url required]
- Interesting files search [--interesting-files/-F] [--url required]
- Thread timeout [--thread-timeout/-T seconds]
- Request timeout [--request-timeout/-rt seconds]


# Format 
I want to add different formats at the future but currently this tool only supports this formats for the input file
```
https://sub.domain.com  
http://sub.domain.com  
sub.domain.com  
.sub.domain.com
```
Which generated by:
- amass  
- aquatone (hosts.txt)  
- subfinder  
- sublist3r  
... and many other subdomain finders  
