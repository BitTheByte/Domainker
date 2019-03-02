from colorama import Fore
import requests
from urllib3.exceptions import InsecureRequestWarning 
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

vuln_msg = "%sVulnerable %s-> %s%s%s"
safe_msg = "%sNot vulnerable"
inject_header  = "controlled-header"
inject_value   = "controlled-value"
inject_payload = "/%0D%0A"

def chkcrlf(url,timeout=30):

    try:
        url = url + "%s%s:%s" % (inject_payload,inject_header,inject_value)

        request = requests.get(url, timeout=timeout,verify=False)

        for header_name, header_value in request.headers.items():
            if header_value == inject_value:
                return vuln_msg % (
                        Fore.GREEN,
                        Fore.YELLOW,
                        Fore.LIGHTWHITE_EX,
                        url,
                        Fore.RESET
                    )


        if request.history:
            for history in request.history:
                for header_name, header_value in history.headers.items():
                    if header_value == inject_value:
                        return vuln_msg % (
                                Fore.GREEN,
                                Fore.YELLOW,
                                Fore.LIGHTWHITE_EX,
                                url,
                                Fore.RESET
                            )
        
        return safe_msg % (Fore.RED)

    except Exception as e:
        return "%sError occured: %s" % (Fore.RED,str(e))
