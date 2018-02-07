# -*- coding:utf-8 -*-

import urllib
import requests


TOKEN_URL = "https://openapi.baidu.com/oauth/2.0/token?grant_type={0}&client_id={1}&client_secret={2}"
TEXT2AUDIO_URL = 'https://tsn.baidu.com/text2audio?tex={0}&lan=zh&cuid={1}&ctp=1&tok={2}&spd={3}&pit={4}&vol={5}&per={6}'
GRANT_TYPE = "client_credentials"
CUID = "XXXXXXXXXXXXX"
Client_id = "XXXXXXXXXXXX"
Secret_key = "XXXXX"


def get_token():
    url = TOKEN_URL.format(GRANT_TYPE, Client_id, Secret_key)
    res = requests.get(url)
    if res.status_code == 200:
        token = res.json()["access_token"]
        with open("token.txt", "w") as f:
            f.write(token)

        return token
    else:
        print (res.json())
        raise Exception(u"获取token失败！！")


def text2audit(text, spd=5, pit=5, vol=6, per=4):
    result = []
    token = get_token()
    while text:
        _text, text = text[:1024], text[1024:]
        _text = urllib.quote(_text)
        url = TEXT2AUDIO_URL.format(_text, CUID, token, spd, pit, vol, per)
        res = requests.get(url)
        if res.headers["Content-Type"] == "audio/mp3":
            result.append(res.content)
        else:
            print res.json()
            raise Exception(u"合成语音错误！！！")

    return b"".join(result)





