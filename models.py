# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:
from peewee import CharField, ForeignKeyField, DateTimeField, TextField, IntegerField, RawQuery
from hashlib import md5
from app import db
import re
import datetime
from dateutil.parser import parse

class User(db.Model):
    name = CharField()
    email = CharField()

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)

class Email(db.Model):
    _from = ForeignKeyField(User, related_name='emails')
    to = CharField()

    subject = CharField()
    text = TextField()

    html = TextField()

    time = DateTimeField()
    thread = IntegerField()

    @classmethod
    def get_thread(cls, subject):
        """ Returns the thread that this subject shoiuld be a part of """
        query = Email.select().where(Email.subject == subject)
        for obj in query:
            return obj.thread
        else:
            query = db.database.execute_sql('SELECT MAX(thread) FROM email')
            result = query.fetchone()
            if result[0] != None:
                return result[0] + 1
            return 1

    def get_time(self):
        if type(self.time) != datetime.datetime:
            self.time = parse(self.time)
        self.time = self.time.replace(tzinfo=None)
        return self.time

class Attachment(db.Model):
    filename = CharField()
    path = CharField()
    email = ForeignKeyField(Email, related_name='attachments')
