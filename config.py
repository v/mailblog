# vim: set expandtab sw=4 ts=4 softtabstop=4 autoindent smartindent:

class Configuration(object):
    DATABASE = {
        'name': 'emails.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'EPIUWYE)WYE&*W&TEFSGDSUHSTU(PWA^*WATGFESDIUASHDK:PD'
    UPLOAD_FOLDER = './uploads'
    SITE_NAME = 'USACS'
    SITE_SLOGAN = 'Undergraduate Student Alliance of Computer Scientists'

class TestConfiguration(object):
    DATABASE = {
        'name': 'test_emails.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'EPIUWYE)WYE&*W&TEFSGDSUHSTU(PWA^*WATGFESDIUASHDK:PD'
    TESTING = True
    UPLOAD_FOLDER = './uploads'
    SITE_NAME = 'USACS'
    SITE_SLOGAN = 'Undergraduate Student Alliance of Computer Scientists'
