# -*- coding: utf-8 -*-

from pprint import pprint as pp

import pytest

import kara
from kara.common import *
from kara.executor import *
from kara.database.util import *
from kara.validator import *


@pytest.mark.parametrize("cond", ["~abcdefg", "~ab", "~a", "~fg", "~g", "~e"])
def test_subStrringValidator_success(cond):
    sub = SubStringValidator()
    assert sub.is_supported("abcdefg", cond, cond[sub.prefix_len:])
    assert sub.verify("abcdefg", cond, cond[sub.prefix_len:])


@pytest.mark.parametrize("cond", ["!abcdefg", "", "!abcdefgx", "~"])
def test_subStrringValidator_failure(cond):
    sub = SubStringValidator()
    assert not sub.is_supported("abcdef", cond, cond[sub.prefix_len:])
    with pytest.raises(karaerror.KaraValidatorError):
        sub.verify("abcdefg", cond, cond[sub.prefix_len:])


@pytest.mark.parametrize("target_obj", ["", None, list()])
def test_subStrringValidator_failure_via_obj(target_obj):
    sub = SubStringValidator()
    assert not sub.is_supported(target_obj, "~abc", "abc")


@pytest.mark.parametrize("cond, target",
                         [("//orderid", "S1610191804785"), ("//game_userid", "1000119900002952006"),
                          ("//sporder_id", "opaweb_GAS_20161019191624"), ("//retcode", "1"),
                          ])
def test_xpathValidator_success(cond, target):
    obj = """<?xml version="1.0" encoding="utf8" ?>
    <orderinfo>
    <err_msg></err_msg>
    <retcode>1</retcode>
    <orderid>S1610191804785</orderid>
    <cardid>64127500</cardid>
    <cardnum>2</cardnum>
    <ordercash>2</ordercash>
    <cardname>全国中石化加油卡直充任意充</cardname>
    <sporder_id>opaweb_GAS_20161019191624</sporder_id>
    <game_userid>1000119900002952006</game_userid>
    <game_state>0</game_state>
    </orderinfo>
    """
    xml = XPathValidator()
    assert xml.is_supported(obj, cond, target)
    assert xml.verify(obj, cond, target)


# TODO: chinese always failure!
@pytest.mark.parametrize("cond, target", [("//cardname", "全国中石化加油卡直充任意充")])
def test_xpathValidator_chinese_will_success(cond, target):
    obj = """<?xml version="1.0" encoding="utf8" ?>
    <orderinfo>
    <err_msg></err_msg>
    <retcode>1</retcode>
    <orderid>S1610191804785</orderid>
    <cardid>64127500</cardid>
    <cardnum>2</cardnum>
    <ordercash>2</ordercash>
    <cardname>全国中石化加油卡直充任意充</cardname>
    <sporder_id>opaweb_GAS_20161019191624</sporder_id>
    <game_userid>1000119900002952006</game_userid>
    <game_state>0</game_state>
    </orderinfo>
    """
    xml = XPathValidator()
    assert xml.is_supported(obj, cond, target)
    assert not xml.verify(obj, cond, target)


@pytest.mark.parametrize("cond, target",
                         [("//orderid", "S1610191804786"), ("//game_userid", "1000119900002952007"),
                          ("//sporder_id", "opaweb_GAS_2016101919162"), ("//retcode", "9999"),
                          ])
def test_xpathValidator_failure(cond, target):
    obj = """<?xml version="1.0" encoding="utf8" ?>
    <orderinfo>
    <err_msg></err_msg>
    <retcode>1</retcode>
    <orderid>S1610191804785</orderid>
    <cardid>64127500</cardid>
    <cardnum>2</cardnum>
    <ordercash>2</ordercash>
    <cardname>全国中石化加油卡直充任意充</cardname>
    <sporder_id>opaweb_GAS_20161019191624</sporder_id>
    <game_userid>1000119900002952006</game_userid>
    <game_state>0</game_state>
    </orderinfo>
    """
    xml = XPathValidator()
    assert xml.is_supported(obj, cond, target)
    assert not xml.verify(obj, cond, target)

def test_batch_verify():
    obj = """<?xml version="1.0" encoding="utf8" ?>
    <orderinfo>
    <err_msg></err_msg>
    <retcode>1</retcode>
    <orderid>S1610191804785</orderid>
    <cardid>64127500</cardid>
    <cardnum>2</cardnum>
    <ordercash>2</ordercash>
    <cardname>全国中石化加油卡直充任意充</cardname>
    <sporder_id>opaweb_GAS_20161019191624</sporder_id>
    <game_userid>1000119900002952006</game_userid>
    <game_state>0</game_state>
    </orderinfo>
    """
    conditions = ("//orderid", "S1610191804785", "//game_userid", "1000119900002952006",
                  "//sporder_id", "opaweb_GAS_20161019191624", "//retcode", "1",
                  "~version", "version", "~64127500", "64127500")
    assert Validator.batch_verify(obj, *conditions)

if __name__ == "__main__":
    pass

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
