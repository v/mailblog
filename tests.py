import requests
from app import db
import json

site_url = 'http://0.0.0.0:8888'

def setup():
    db.database.execute_sql("DELETE FROM email")
    db.database.execute_sql("DELETE FROM user")

def mock_sendgrid():
    payload = open('sample_payload.json').read()

    r = requests.post(site_url+'/callback', data=payload)
    print r.text
    assert r.status == 200

def mock_email(name, email, subject, text, html=None):
    if not html:
        html = text

    email_object = {
        'from': '%s <%s>' % (name, email),
        'html': html,
        'subject': subject,
        'text': text,
    }

    r = requests.post(site_url+'/callback', data=json.loads(email_object))
    print r.text
    assert r.status == 200

mock_email('herp', 'herp@herp.com', 'Herp Subject', 'Childish gambinooo')
