import requests
from app import db

site_url = 'http://0.0.0.0:8888'

def setup():
    db.database.execute_sql("DELETE FROM email")
    db.database.execute_sql("DELETE FROM user")


def mock_sendgrid():
    payload = open('sample_payload.json').read()

    r = requests.post(site_url+'/callback', data=payload)
    print r.text
    assert r.status == 200

def mock_email():
