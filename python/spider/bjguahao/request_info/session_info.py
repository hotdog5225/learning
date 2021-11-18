import requests

class SessionInfo:
    def __init__(self, header_info, cookie_info):
        self.header_info = header_info
        self.cookie_info = cookie_info

    def getGeneralSession(self):
        # cookie_dict = self.cookie_info.get_general_cookie()
        # cookie_jar = http.cookiejar.CookieJar()

        headers = self.header_info.getGeneralHeader()

        session = requests.Session()
        session.headers = headers

        # session.cookies = requests.utils.add_dict_to_cookiejar(cookie_jar, cookie_dict)
        return session