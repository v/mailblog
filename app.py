""" This file sets up the Flask Application for sniper.
    Sniper is an application that hits the Rutgers SOC API and notifies users when a class opens up. """

from flask import Flask, request
import json
import re
from flask_peewee.db import Database

# Set up the Flask application
app = Flask(__name__)
app.config.from_object('config.Configuration')
app.config.from_envvar('EMAILCLASS')

db = Database(app)

from peewee import CharField, ForeignKeyField, DateTimeField, TextField, IntegerField, RawQuery
from hashlib import md5
import datetime

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
        query = RawQuery(Email, 'SELECT * FROM email WHERE subject LIKE "%%%s%%"' % (subject))
        for obj in query.execute():
            return obj.thread
        else:
            query = db.database.execute_sql('SELECT MAX(thread) FROM email')
            result = query.fetchone()
            if result[0]:
                return result[0] + 1
            return 0

@app.route('/', methods=['GET', 'POST'])
def home():
    """ Handles the home page rendering."""
    return 'Hello usacs'


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    """ Handles the home page rendering."""
    data = json.loads(request.data)

    email_from = data['from']
    name, email = parse_email(email_from) 
    
    user = User.get_or_create(name=name, email=email)
    thread=Email.get_thread(data['subject'])

    email = Email(
            _from=user, 
            to=data['to'], 
            subject=data['subject'], 
            text=data['text'], 
            html=data['html'], 
            time=datetime.datetime.now(), 
            thread=thread,
        )

    email.save()
    return 'Thanks Swift'

def parse_email(text):
    m = re.search('(.+)<(.+)>', text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None

if __name__=='__main__':
    app.run('0.0.0.0', port=8888, debug=True)

