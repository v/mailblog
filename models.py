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
    reply_regex = re.compile('[Rr][Ee]\:')
    fwd_regex = re.compile('[Ff][Ww][Dd]*\:')
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
        subject = re.sub(cls.reply_regex, '', subject).strip()
        subject = re.sub(cls.fwd_regex, '', subject).strip()
        query = RawQuery(Email, 'SELECT * FROM email WHERE subject LIKE "%%%s%%"' % (subject))
        for obj in query.execute():
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
        return self.time
