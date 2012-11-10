# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:
""" This file sets up the Flask Application for sniper.
    Sniper is an application that hits the Rutgers SOC API and notifies users when a class opens up. """

from flask import Flask, request, render_template
from flask_peewee.db import Database
from peewee import RawQuery

import json
import re
import os
import datetime
import math

POSTS_PER_PAGE = 10

# Set up the Flask application
app = Flask(__name__)
app.config.from_object('config.Configuration')
if 'EMAILCLASS' in os.environ:
    app.config.from_object(os.environ['EMAILCLASS'])

db = Database(app)
from models import User, Email

@app.route('/', methods=['GET', 'POST'], defaults={'page_num' : 1})
@app.route('/<int:page_num>', methods=['GET', 'POST'])
def home(page_num):
    """ Handles the home page rendering."""
    thread_id_query = 'SELECT DISTINCT thread FROM email LIMIT %d, %d' % \
            (POSTS_PER_PAGE*(page_num-1), POSTS_PER_PAGE)
    thread_ids = [email.thread for email in RawQuery(Email, thread_id_query)]

    threads_query = 'SELECT * FROM email WHERE thread IN %s ORDER BY thread' % str(tuple(thread_ids))
    all_threads = RawQuery(Email, threads_query)

    num_pages = math.ceil(Email.select().group_by(Email.thread).count()/float(POSTS_PER_PAGE))
    threads = []

    last_thread_id = None

    for email in all_threads:
        thread_id = email.thread
        if thread_id != last_thread_id:
            threads.append([])
        threads[-1].append(email)
        last_thread_id = thread_id
    return render_template('home.html', threads=threads, page_num=page_num, num_pages=num_pages)


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
