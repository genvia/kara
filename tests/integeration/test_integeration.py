# -*- coding: utf-8 -*-

from pprint import pprint as pp

import kara
from kara.executor import *
from kara.database.util import *
from kara.validator import *

def test_allinone():
    opa = OpaStdHTTPExecutor("onlineorder.do", "opa_std_hf.py")
    result = opa.invoke()
    assert Validator.batch_verify(opa.resp_text, "//retcode", "1", "//sporder_id", opa.oflinkid)
    maindb = kara.opened_dbs['main']
    sql = str(Select("salebilltable", ["oflinkid=" + opa.oflinkid, "usercode=" + opa.userid, "cash=1"]))
    print sql
    bill = maindb.fetch(sql)
    assert len(bill) == 1
    assert bill.oflinkid == opa.oflinkid
    assert bill.billid == opa.billid
    assert bill.usercode == opa.userid

# def test_insert_crm():
#     with Database(kara.conf.dbs.crm.url) as crm:
#         for i in xrange(10000):
#             orderid = "C20161019{:08d}".format(i)
#             sql = str(Insert("OFCS_CONSULT_ORDER",ORDER_ID=orderid, CUSTOMER_TYPE='INTERNET_BAR', END_TIME='sysdate-8:n', CUSTOMER_CODE='A19760216', CONSULT_TYPE='1600', ADD_TIME='sysdate-8:n', CHANNEL='ONLINE', FEEDBACK_ACCOUNT='13913850116', EXT2='null', COMMENTS='release notice', EXT1='null', CONSULT_SUB_TYPE='1605', RECEPTION_NAME='pangdinghai', RECEPTION_CODE='of656', ORDER_TYPE='GAS_CARD' ))
#             effected = crm.execute(sql)
#             assert effected.rowcount == 1

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
