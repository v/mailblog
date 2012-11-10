# config

class Configuration(object):
    DATABASE = {
        'name': 'emails.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'EPIUWYE)WYE&*W&TEFSGDSUHSTU(PWA^*WATGFESDIUASHDK:PD'


class TestConfiguration(object):
    DATABASE = {
        'name': 'test_emails.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'EPIUWYE)WYE&*W&TEFSGDSUHSTU(PWA^*WATGFESDIUASHDK:PD'
    TESTING = True
