# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:
""" This file sets up the Flask Application for sniper.
    Sniper is an application that hits the Rutgers SOC API and notifies users when a class opens up. """

from flask import Flask, request, render_template
from flask_peewee.db import Database
from peewee import RawQuery
from bs4 import BeautifulSoup
from dateutil.parser import parse

import json
import re
import os
import datetime
import math
import ago

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
    thread_id_query = 'SELECT DISTINCT thread FROM email ORDER BY time DESC LIMIT %d, %d' % \
            (POSTS_PER_PAGE*(page_num-1), POSTS_PER_PAGE)
    thread_ids = [email.thread for email in RawQuery(Email, thread_id_query)]

    threads = []
    for thread_id in thread_ids:
        emails_query = 'SELECT * FROM email WHERE thread = %d ORDER BY time ASC' % thread_id
        threads.append([email for email in RawQuery(Email, emails_query)])

    num_pages = math.ceil(Email.select().group_by(Email.thread).count()/float(POSTS_PER_PAGE))

    return render_template('home.html', threads=threads, page_num=page_num, num_pages=num_pages)


@app.route('/callback', methods=['GET', 'POST'])
def callback():

    """ Handles the home page rendering."""
    data = json.loads(request.data)

    email_from = data['from']
    name, email = parse_email(email_from) 
    
    user = User.get_or_create(name=name, email=email)
    thread=Email.get_thread(data['subject'])

    if 'time' in data:
        time = parse(data['time'])
    else:
        time = datetime.datetime.now()

    email = Email(
            _from=user, 
            to=data['to'], 
            subject=data['subject'], 
            text=data['text'], 
            html=data['html'], 
            time=time,
            thread=thread,
        )

    email.save()
    return 'Thanks Swift'

def parse_email(text):
    m = re.search('(.+)<(.+)>', text)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text, text

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'table', 'tr', 'td', 'b', 'i', 'a']
def sanitize_html(value):
    try:
        soup = BeautifulSoup(value)

        for tag in soup.find_all(True):
            if tag.name == 'a' and tag.attrs.has_key('href'):
                tag.attrs = tag.attrs = {
                    'href' : tag.attrs['href']
                }
            else:
                tag.attr = {}
            if tag.name not in VALID_TAGS:
                tag.hidden = True

        return soup.renderContents()
    except:
        return value

app.jinja_env.filters['sanitize'] = sanitize_html
app.jinja_env.filters['human_time'] = ago.human

