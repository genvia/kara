# -*- coding: utf-8 -*-

import pytest
from pprint import pprint as pp

import kara
from kara.executor import *
from kara.database.util import *
from kara.validator import *

def test_ofrg_fetchorder_executor_fetch_one():
    ofrg_fetch = OfrgFetchOrderHTTPExecutor(
        kara.conf.uts.ofrg.host)
    result = ofrg_fetch.invoke({'num': 2, 'supUid': 'yczc006'})
    pp(ofrg_fetch.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


@pytest.mark.parametrize('num', [1, 3])
def test_ofrg_fetchorder_executor_fetch_multi(num):
    ofrg_fetch = OfrgFetchOrderHTTPExecutor(
        kara.conf.uts.ofrg.host)
    payload = dict()
    payload['supUid'] = 'yczc001'
    payload['num'] = num
    result = ofrg_fetch.invoke(payload)
    pp(ofrg_fetch.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


# bucause orderid is final state, will always callback failure. so mocking.
from httmock import urlmatch, HTTMock


@urlmatch(netloc=kara.conf.uts.ofrg.host + ":" + kara.conf.uts.ofrg.port)
def callback_mock(url, request):
    return "success"


def test_ofrg_callback_executor_cancel():
    ofrg_callback = OfrgCallbackHTTPExecutor(
        kara.conf.uts.ofrg.host, "cancelOrder")
    with HTTMock(callback_mock):
        result = ofrg_callback.invoke({'orderid': 'S1610198680794',
                                       'supuid': 'yczc001'})
    pp(ofrg_callback.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


def test_ofrg_callback_executor_failure():
    ofrg_callback = OfrgCallbackHTTPExecutor(
        kara.conf.uts.ofrg.host, "againOrder")
    with HTTMock(callback_mock):
        result = ofrg_callback.invoke({'orderid': 'S1610188680774',
                                       'supuid': 'yczc001'})
    pp(ofrg_callback.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


def test_ofrg_callback_executor_success():
    ofrg_callback = OfrgCallbackHTTPExecutor(
        kara.conf.uts.ofrg.host, "successOrder")
    with HTTMock(callback_mock):
        result = ofrg_callback.invoke({'orderid': 'S1610198680796',
                                       'supuid': 'yczc001'})
    pp(ofrg_callback.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


def test_ofrg_callback_executor_unknown():
    ofrg_callback = OfrgCallbackHTTPExecutor(
        kara.conf.uts.ofrg.host, "unKnownReturn")
    with HTTMock(callback_mock):
        result = ofrg_callback.invoke({'orderid': 'S1610188680786',
                                       'supuid': 'yczc001'})
    pp(ofrg_callback.raw)
    pp(result.status_code)
    pp(result.text)
    assert result.status_code == 200
    # assert 0


if __name__ == "__main__":
    pass

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
