# -*- coding:utf-8 -*-

import urllib
import requests


TOKEN_URL = "https://openapi.baidu.com/oauth/2.0/token?grant_type={0}&client_id={1}&client_secret={2}"
TEXT2AUDIO_URL = 'https://tsn.baidu.com/text2audio?tex={0}&lan=zh&cuid={1}&ctp=1&tok={2}&spd={3}&pit={4}&vol={5}&per={6}'
GRANT_TYPE = "client_credentials"
CUID = "dengwenyue123"
Client_id = "Xmb1lGy8THbzcozXt0mQhpWP"
Secret_key = "8ae1fc7365113f12115cf94ebec0e770"


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


# with open("/tmp/第2章.txt", 'r') as f:
#     text = f.read()
#
# print text
# print type(text)
text = "亚麻跌" * 50
audio = text2audit(text=text)


with open("test.mp3", "wb") as f:
    f.write(audio)



