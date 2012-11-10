# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:
""" This file sets up the Flask Application for sniper.
    Sniper is an application that hits the Rutgers SOC API and notifies users when a class opens up. """

from flask import Flask, request, render_template
import json
import re
from flask_peewee.db import Database

import os

# Set up the Flask application
app = Flask(__name__)
app.config.from_object('config.Configuration')
if 'EMAILCLASS' in os.environ:
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
    reply_regex = re.compile('[Rr][Ee]\:')
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
    all_threads = RawQuery(Email, 'SELECT * FROM email ORDER BY thread DESC')
    threads = []

    last_thread_id = None

    for email in all_threads:
        thread_id = email.thread
        if thread_id != last_thread_id:
            threads.append([])
        threads[-1].append(email)
        last_thread_id = thread_id
    return render_template('home.html', threads=threads)


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

