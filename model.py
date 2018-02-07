# -*- coding:utf-8 -*-
import datetime
from my_story import db


class Book(db.Model):

    __tablename__ = "books"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    uuid = db.Column(db.String)

    @classmethod
    def get_book_id(cls, name):
        book = cls.query.filter_by(cls.name == name).first()
        return book.uuid if book else ""


class Page(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    prev_page = db.Column(db.String)
    next_page = db.Column(db.String)
    book_uuid = db.Column(db.String)

    @classmethod
    def get_prev_and_next(cls, name):
        curr_page = cls.query.filter_by(cls.name == name).first()
        if curr_page:
            return curr_page.prev_page, curr_page.next_page
        else:
            return "", ""


class Token(db.Model):
    __tablename__ = "token"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    token = db.Column(db.String)
    gen_time = db.Column(db.DateTime)
    out_time = db.Column(db.Integer)

    @classmethod
    def get_token(cls):
        return cls.query.first().token

    @classmethod
    def is_outted(cls, now):
        if cls.gen_time + datetime.timedelta(seconds=cls.out_time) < now:
            return False
        else:
            return True





