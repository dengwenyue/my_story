# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
# from Queue import Queue

URL = "https://www.qu.la"

app = Flask(__name__, static_folder="/tmp")
app.config.from_object(Config)
db = SQLAlchemy(app)

from model import *   # noqa

# db.create_all()


def __init_db():
    str_format = u"第%s章"
    for i in range(1, 1001):
        curr_page = str_format % i
        if i == 1:
            prev_page = None
        else:
            prev_page = str_format % (i-1)
        next_page = str_format % (i+1)
        print curr_page
        page = Page(name=curr_page, prev_page=prev_page, next_page=next_page, book_uuid="11517")
        db.session.add(page)
    db.session.commit()

    book = Book(name=u"单兵为王", uuid="11517")
    db.session.add(book)
    db.session.commit()


# __init_db()