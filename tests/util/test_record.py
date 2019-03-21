# -*- coding: utf-8 -*-

import os

import pytest
from pprint import pprint as pp

import kara
from kara.executor import *
from kara.database.util import *
from kara.validator import *


##############################
def test_database_connect():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True

def test_database_transaction():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        # start transaction
        trans = ofrc.begin()

        # insert one record
        sql = str(Insert("mb_config", mid='kara_trans', key='kara1mid_trans', value='kara1value_trans'))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1

        # fetch it, should get it
        sql = str(Select("mb_config", "mid='kara_trans'"))
        rec = ofrc.fetch(sql)
        assert rec.mid   == "kara_trans"
        assert rec.key   == "kara1mid_trans"
        assert rec.value == "kara1value_trans"
        assert len(rec) == 1

        # rollback transaction
        trans.rollback()

        # fetch it again, should get nothing
        sql = str(Select("mb_config", "mid='kara_trans'"))
        rec = ofrc.fetch(sql)
        assert rec == None


def test_database_insert_mbconfig():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True

        # insert
        sql = str(Insert("mb_config", mid='kara1', key='kara1mid', value='kara1value'))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1
        # fetch it
        sql = str(Select("mb_config", "mid='kara1'"))
        rec = ofrc.fetch(sql)
        assert rec.mid   == "kara1"
        assert rec.key   == "kara1mid"
        assert rec.value == "kara1value"
        assert len(rec) == 1
        # delete
        sql = str(Delete("mb_config", "mid='kara1'"))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1

def test_database_fetchone_mbconfig():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True

        # insert
        sql = "INSERT INTO mb_config VALUES ('kara9',  'kara9mid', 'kara9value')"
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1

        # fetch it
        sql = str(Select("mb_config", "mid='kara9'"))
        rec = ofrc.fetch(sql)
        assert rec.mid   == "kara9"
        assert rec.key   == "kara9mid"
        assert rec.value == "kara9value"
        assert len(rec) == 1

        # update
        sql = str(Update("mb_config", "mid='kara9'", key="xx", value="www"))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1

        # fetch it
        sql = str(Select("mb_config", "mid='kara9'"))
        rec = ofrc.fetch(sql)
        assert rec.mid   == "kara9"
        assert rec.key   == "xx"
        assert rec.value == "www"
        assert len(rec) == 1

        # delete
        sql = str(Delete("mb_config", "mid='kara9'"))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1


def test_database_fetch_multi_mbconfig():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True

        # insert
        sql = "INSERT INTO mb_config VALUES ('karaZ',  'karaAmid', 'karaAvalue')"
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1
        sql = "INSERT INTO mb_config VALUES ('karaZ',  'karaBmid', 'karaBvalue')"
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1
        sql = "INSERT INTO mb_config VALUES ('karaZ',  'karaCmid', 'karaCvalue')"
        effected = ofrc.execute(sql)
        assert effected.rowcount == 1

        # fetch multiply rows
        sql = str(Select("mb_config", where=["mid LIKE 'karaZ'", "key LIKE 'kara%mid'"], order="key"))
        rows = ofrc.fetch(sql, fetchall=True)
        for index, row in enumerate(rows):
            if index == 0:
                assert row.mid   == "karaZ"
                assert row.key   == "karaAmid"
                assert row.value == "karaAvalue"
            elif index == 1:
                assert row.mid   == "karaZ"
                assert row.key   == "karaBmid"
                assert row.value == "karaBvalue"
            elif index == 2:
                assert row.mid   == "karaZ"
                assert row.key   == "karaCmid"
                assert row.value == "karaCvalue"
            else:
                raise ValueError("wtf?")
        assert len(rows) == 3

        # delete
        sql = str(Delete("mb_config", "mid='karaZ'"))
        effected = ofrc.execute(sql)
        assert effected.rowcount == 3

def test_database_execute_single_sql():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True
        sql = "update T_SUPUSER set hasfapiao='1' where supuid like 'provider%'"
        effected = ofrc.execute(sql)
        assert effected > 0

def test_database_execute_single_sql_with_placeholder():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True
        sql = "update T_SUPUSER set hasfapiao=:fp where supuid = :uid"
        effected = ofrc.execute(sql, fp='1', uid='providerId100')
        assert effected > 0

def test_database_execute_single_sql_with_placeholder_2():
    url = kara.conf.dbs.ofrc.url
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True
        sql = "update T_SUPUSER set hasfapiao=:fp where supuid like :uid"
        effected = ofrc.execute(sql, fp='1', uid='providerId%')
        assert effected > 0

def test_database_execute_sql_file():
    url = kara.conf.dbs.ofrc.url
    absulte_path = os.path.join(kara.KARA_HOME, kara.SQL_FILE_DIR, "clean_ofrg_orders.sql")
    with Database(url, echo=False) as ofrc:
        assert ofrc.connected == True
        effected = ofrc.execute_sql_file(absulte_path)

    assert len(effected) == 2


def test_database_execute_sql_file_with_placeholder():
    content = """-- SQL file for kara Database object require:
--   1. one sql statement must completely be in one line.
--   2. can comment use '--' or '#', but have to comment at first column
--   3. ';' at end of one line is optional.
--   4. empty line is ignored.
--   5. file encoding must be utf-8

# change ofrc@t_sys_orders orders state
UPDATE t_sys_orders SET state=:state WHERE addtime>trunc(sysdate-:day,'dd');

-- change ofrc@t_sys_orders orders state
UPDATE t_recharge_order SET state=:state WHERE addtime>trunc(sysdate-:day,'dd');
    """

    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        f.write(content)
        f.flush()
        url = kara.conf.dbs.ofrc.url
        with Database(url, echo=False) as ofrc:
            assert ofrc.connected == True
            effected = ofrc.execute_sql_file(f.name, state=13, day=1)
        assert len(effected) == 2

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
