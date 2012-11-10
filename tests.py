# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:
import requests
import sys
import os
if 'EMAILCLASS' not in os.environ:
    print 'You need to set EMAILCLASS before running tests'
    print 'export EMAILCLASS=config.TestConfiguration'
    sys.exit(1)
    
from app import app, db
from models import User, Email
import json
import unittest
from peewee import RawQuery

site_url = 'http://0.0.0.0:8888'

class MailBlogTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

        User.create_table()
        Email.create_table()

    def tearDown(self):
        User.drop_table()
        Email.drop_table()

    def test_sendgrid(self):
        payload = open('sample_payload.json').read()
        rv = self.app.post('/callback', data=payload)
        print rv.data
        assert rv.status_code == 200

    def mock_email(self, name, email, to, subject, text, html=None):
        if not html:
            html = text

        email_object = {
            'from': '%s <%s>' % (name, email),
            'html': html,
            'subject': subject,
            'text': text,
            'to': to,
        }

        rv = self.app.post('/callback', data=json.dumps(email_object))
        assert rv.status_code == 200

    def test_email_receive(self):
        """ Makes sure that when we receive an email we properly create a user and email object with the appropriate attributes"""
        self.mock_email('Name', 'email@emails.com', 'to@emails.com', 'Derp Subject', 'text')

        users = User.select()
        emails = Email.select()

        assert users.count() == 1
        assert emails.count() == 1

        email = emails.get()
        user = users.get()

        assert user.name == 'Name'
        assert user.email == 'email@emails.com'
        assert email._from == user
        assert email.to == 'to@emails.com'
        assert email.subject == 'Derp Subject'
        assert email.text == 'text'
        assert email.html == 'text'
    
    def test_email_from_one_user(self):
        """ We should use the same user object from multiple emails"""
        self.mock_email('Name', 'email@emails.com', 'to@emails.com', 'Derp Subject', 'text')
        self.mock_email('Name', 'email@emails.com', 'to@emails.com', 'Second Subject', 'text on text')

        users = User.select()
        emails = Email.select()

        assert users.count() == 1
        assert emails.count() == 2

        user = users.get()

        assert user.name == 'Name'
        assert user.email == 'email@emails.com'
    
    def test_emails_thread_properly(self):
        """ Makes sure that when we receive multiple emails with reply subjects, we properly put them in the same thread"""

        froms = [
            ('Derp', 'derp@derpina.com'),
            ('Herp', 'herp@derpina.com'),
        ]

        to = 'usacs@sendgriddemos.com'

        subject = 'Derping the Herp'
        different_subject = 'Not Derping the Herp'
        text = 'AINT NOBODY GOT TIME FO DAT'

        self.mock_email(froms[0][0], froms[0][1], to, subject, text)

        for i in range(0, 10):
            _from = froms[i % len(froms)]

            if i % 2 == 0:
                herp = 'Re: '
            else:
                herp = 'Fw: '

            reply_subject = herp*i + subject
            
            self.mock_email(_from[0], _from[1], to, reply_subject, text)

        users = User.select()
        assert users.count() == len(froms)

        emails = Email.select()
        assert emails.count() == 11

        first_email = emails.get()

        for email in emails:
            assert email.thread == first_email.thread

        self.mock_email(froms[0][0], froms[0][1], to, different_subject, text)

        thread_query = RawQuery(Email, 'SELECT * FROM email WHERE thread != %d' % first_email.thread)

        result = thread_query.execute()
        assert len(list(result)) == 1

def mock_email(name, email, to, subject, text, html=None):
    if not html:
        html = text

    email_object = {
        'from': '%s <%s>' % (name, email),
        'html': html,
        'subject': subject,
        'text': text,
        'to': to,
    }

    r = requests.post(site_url+'/callback', data=json.dumps(email_object))
    print r.text
    assert r.status_code == 200
if __name__ == '__main__':
    unittest.main()
