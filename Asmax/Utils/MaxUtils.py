import datetime
import random

from UserAgenter import UserAgent


class MaxUtils:
    global_ver = 11
    global_android_version = "25.7.2"
    global_web_version = "25.8.4"
    lang_code = "cz"
    timezone = "Europe/Paris"
    screen = "1080x1920 1.0x"
    platform = "WEB"

    @staticmethod
    def random_str(length):
        letters = "abcdef1234567890"
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def random_useragent(type: int = 0):
        if type == 0: # android
            return UserAgent().RandomAndroidAgent()
        if type == 1: # web
            return UserAgent().RandomEdgeAgent()

    @staticmethod
    def get_timestamp():
        return int(datetime.datetime.now().timestamp())