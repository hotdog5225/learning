import time

class CookieInfo:
    def get_generatl_cookie(self):
        # return 'imed_session=VVk0fFRruSBjstSIpGYU4nMPscSYyGwJ_5456625; __jsluid_s=dabfd1d9f43e257e39dd26d63435425c; SECKEY_CID=1e04a5a2e21f660e8089f7a18b959883073f14ce; secure-key=470cd0b3-67bd-4ce6-8c0c-748695ba0d6a; agent_login_img_code=1831bf4473234a8db01a6b3c68c68ebf; imed_session=VVk0fFRruSBjstSIpGYU4nMPscSYyGwJ_5456625; BMAP_SECKEY=646f10cb77181888e7eef50bc07d45274c5fe0c85c4ae6a2b8a66de6bcc21f3371287d727a5322140481ce64c70ad1b657a6e09c31496fd4129b0c48c0873df5e65fdd5dad42907939e1c29f1e11ff580221bd14f507d16fad988972b921284165fbbccef2db3357a30d08caba9a19fde94ef470f4f623ab8c13f4b4037537b3877460529a672b3d9de110f6bd7e61ce6b6d38304f34b87c3ed5b1afce5c569321c6b3bf58c20466a9b28392417fe511a0e4199d1693ff1862dc23fc3ca703b673a3ee53ed8dbaeb961d1a7b3d76046cd05ab7319cbf4408e6890e63b0da153be89792c391881f953c5ec5ee3c1a2879; cmi-user-ticket=UE0-fcCBKgwrQWYlTTfseXy_6K-O1SJJCHsRag..; imed_session_tm={}'.format(
        #     str(int(time.time()) * 1000))

        # get cookie manually
        # TODO set cookie manually
        origin_cookie_str = 'imed_session=VVk0fFRruSBjstSIpGYU4nMPscSYyGwJ_5456625; __jsluid_s=dabfd1d9f43e257e39dd26d63435425c; SECKEY_CID=1e04a5a2e21f660e8089f7a18b959883073f14ce; secure-key=470cd0b3-67bd-4ce6-8c0c-748695ba0d6a; agent_login_img_code=1831bf4473234a8db01a6b3c68c68ebf; imed_session=VVk0fFRruSBjstSIpGYU4nMPscSYyGwJ_5456625; BMAP_SECKEY=646f10cb77181888e7eef50bc07d45274c5fe0c85c4ae6a2b8a66de6bcc21f3371287d727a5322140481ce64c70ad1b657a6e09c31496fd4129b0c48c0873df5e65fdd5dad42907939e1c29f1e11ff580221bd14f507d16fad988972b921284165fbbccef2db3357a30d08caba9a19fde94ef470f4f623ab8c13f4b4037537b3877460529a672b3d9de110f6bd7e61ce6b6d38304f34b87c3ed5b1afce5c569321c6b3bf58c20466a9b28392417fe511a0e4199d1693ff1862dc23fc3ca703b673a3ee53ed8dbaeb961d1a7b3d76046cd05ab7319cbf4408e6890e63b0da153be89792c391881f953c5ec5ee3c1a2879; cmi-user-ticket=UE0-fcCBKgwrQWYlTTfseXy_6K-O1SJJCHsRag..; imed_session_tm={}' \
            .format(str(int(time.time()) * 1000))
        cookie_dict = {}
        cookie_list = origin_cookie_str.split('; ')
        for cookie in cookie_list:
            cookie_dict[cookie.split('=')[0]] = cookie.split('=')[1]

        return cookie_dict
