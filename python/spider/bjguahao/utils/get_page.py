import requests


def get_page(url):
    session = requests.Session()
    session.headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    resp = session.get(url, verify=False)
    if resp.status_code != 200:
        raise ValueError("http code not 200")
    return resp.content.decode('utf-8')
