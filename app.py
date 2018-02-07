# -*- coding:utf-8 -*-

import os
import requests
import datetime
import urllib
from my_story import app, db
from flask import render_template, request
from my_story import Book, Page, Token


@app.route("/index")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/contents")
def contents():
    book_uuid = request.args.get("uuid")
    if not book_uuid:
        return u"找不到对应的书籍"
    cons = db.session.query(Page).filter(Page.book_uuid == book_uuid).all()
    return render_template("contents.html", contents=cons)


@app.route("/text")
def get_text():
    page = request.args.get("page")
    if not page:
        return u"已经没有内容了"
    filename = page + ".txt"
    filepath = os.path.join("/tmp", filename)
    with open(filepath) as f:
        cont = f.readlines()
    cont = [c.decode("utf-8") for c in cont]
    page = Page.query.filter_by(name=page).first()
    return render_template("text.html", cont=cont, page=page)


@app.route("/audio")
def get_audio():
    page = request.args.get("page")
    if not page:
        return u"找不到对应页"
    audio_name = page + ".mp3"
    audit_path = os.path.join("/tmp", audio_name)
    if not os.path.exists(audit_path):
        filename = page + ".txt"
        filepath = os.path.join("/tmp", filename)
        with open(filepath) as f:
            text = f.read()

        audio = text2audit(text=text)

        with open(audit_path, "wb") as f:
            f.write(audio)
    return render_template("audio.html", uri=audit_path)


def text2audit(text, spd=5, pit=5, vol=6, per=4):
    result = []
    token = get_token()

    while text:
        _text, text = text[:1024], text[1024:]
        _text = urllib.quote(_text)
        url = app.config["TEXT2AUDIO_URL"].format(_text, app.config["CUID"], token, spd, pit, vol, per)
        res = requests.get(url)
        if res.headers["Content-Type"] == "audio/mp3":
            result.append(res.content)
        else:
            print res.json()
            raise Exception(u"合成语音错误！！！")

    return b"".join(result)


def get_token():
    url = app.config["TOKEN_URL"].format(app.config["GRANT_TYPE"], app.config["CLIENT_ID"], app.config["AIP_SECERT_KEY"])
    res = requests.get(url)
    if res.status_code == 200:
        token = res.json()["access_token"]
        gen_time = datetime.datetime.now()
        out_time = int(res.json()["expires_in"])
        db.session.add(Token(token=token, gen_time=gen_time, out_time=out_time))
        db.session.commit()

        return token
    else:
        print (res.json())
        raise Exception(u"获取token失败！！")


app.run(host="0.0.0.0", port=18888, debug=True)





