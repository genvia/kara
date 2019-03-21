# -*- coding: utf-8 -*-

import os
import atexit

# checking KARA_HOME environment
KARA_HOME = os.environ.get("KARA_HOME")

if not KARA_HOME or not os.path.isdir(KARA_HOME):
    raise RuntimeError("Oops! not found KARA_HOME environment.")

PARAM_FILE_DIR = 'params'
SQL_FILE_DIR   = os.path.join(PARAM_FILE_DIR, 'sql')
LOGS_FILE_DIR  = 'logs'
CONF_FILE_DIR  = 'conf'

# load config
from config import Config
conf = Config(os.path.join(KARA_HOME, CONF_FILE_DIR, "kara.cfg"))

# for kara logging
if conf.common.logging:
    from logbook import Logger, TimedRotatingFileHandler
    tmppath = os.path.join(KARA_HOME, LOGS_FILE_DIR, "kara.log")
    handler = TimedRotatingFileHandler(tmppath, date_format='%Y-%m-%d')
    handler.push_application()
else:
    class Logger(object):
        def __init__(self, name, level=0):
            self.name = name
            self.level = level
        debug = info = warn = warning = notice = error = exception = \
            critical = log = lambda *a, **kw: None

# for inspect kara log start point
CLIENT_CATEGORY = CLIENT_ID = "KARA"
def logging_client_running_id(client_category):
    import uuid
    global CLIENT_CATEGORY, CLIENT_ID, logger, Logger

    CLIENT_ID       = str(uuid.uuid1()).upper()
    CLIENT_CATEGORY = client_category

    logger = Logger(CLIENT_CATEGORY)
    logger.info("*" * 80)
    logger.info("*{}{}{}*".format(" " * ((78 - len(CLIENT_ID)) / 2), CLIENT_ID, " " * ((78 - len(CLIENT_ID)) / 2)))
    logger.info("*" * 80)

    return CLIENT_ID


# not running under a client
logger = Logger(CLIENT_CATEGORY)
logger.info("={}{}{}=".format("=" * ((78 - len(CLIENT_ID)) / 2), CLIENT_ID, "=" * ((78 - len(CLIENT_ID)) / 2)))

# why place here, but not under 'del _subdirs' ?
from . import common
from . import executor
from . import validator
from . import dataset
from . import database

# _subdirs = lambda *dirs: [os.path.abspath(os.path.join(__path__[0], sub)) for sub in dirs]
# __path__ = _subdirs('common', 'util', 'waiter')
# del _subdirs
# in common/util/waiter directory' modules, can import by:
# import kara
# from kara import xxx

# connect all database
opened_dbs = {}
def _connect_all_database(opened_dbs):
    for key in conf.dbs.keys():
        opened_dbs[key] = database.util.Database(conf.dbs[key]['url'])
_connect_all_database(opened_dbs)

# when system exit, close all database
def _close_database_when_exit(database_dict):
    import kara
    for k, v in database_dict.items():
        if isinstance(v, database.util.Database) and v.connected:
            v.close()
            kara.logger.info("{} database was closed, connected state was [{}].".format(k, v.connected))
atexit.register(_close_database_when_exit, opened_dbs)

if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

