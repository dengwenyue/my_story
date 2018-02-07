# -*- coding:utf-8 -*-


class Config(object):
    SECRET_KEY = "my test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///my_story.db"
    TOKEN_URL = "https://openapi.baidu.com/oauth/2.0/token?grant_type={0}&client_id={1}&client_secret={2}"
    TEXT2AUDIO_URL = 'https://tsn.baidu.com/text2audio?tex={0}&lan=zh&cuid={1}&ctp=1&tok={2}&spd={3}&pit={4}&vol={5}&per={6}'
    GRANT_TYPE = "client_credentials"
    CUID = "XXXXXXX"
    CLIENT_ID = "XXXXXXX"
    AIP_SECERT_KEY = "XXXXXXX"
