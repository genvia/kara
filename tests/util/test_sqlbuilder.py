# -*- coding: utf-8 -*-

import pytest
from pprint import pprint as pp

import kara
from kara.database.util.sqlbuilder import WhereClause
from kara.database.util.sqlbuilder import FromClause
from kara.database.util.sqlbuilder import OrderbyClause
from kara.database.util.sqlbuilder import GroupbyClause
from kara.database.util.sqlbuilder import Select
from kara.database.util.sqlbuilder import Delete
from kara.database.util.sqlbuilder import Update
from kara.database.util.sqlbuilder import Insert


##############################
def test_from0():
    f = FromClause('a', '>b', on='a.id == b.id')
    assert str(f) == "FROM a RIGHT JION b ON a.id == b.id"


def test_from1():
    f = FromClause('a', '#b')
    assert str(f) == "FROM a JOIN b"


def test_from2():
    f = FromClause('t_product', '>t_product_price')
    assert str(f) == "FROM t_product RIGHT JION t_product_price"


def test_from3():
    f = FromClause('saleuser', '<saleuser_info')
    assert str(f) == "FROM saleuser LEFT JION saleuser_info"


def test_from4():
    f = FromClause('t_sys_orders', 't_recharg_order')
    assert str(f) == "FROM t_sys_orders JOIN t_recharg_order"

##############################


def test_where0():
    with pytest.raises(ValueError):
        WhereClause()
    with pytest.raises(ValueError):
        WhereClause("")
    with pytest.raises(ValueError):
        WhereClause("x", "")


def test_where1():
    w = WhereClause("oflinkid=?")
    assert str(w) == "WHERE oflinkid='?'"


def test_where2():
    w = WhereClause("oflinkid= ?   ", "saleuser:n =?")
    assert str(w) == "WHERE oflinkid='?' AND saleuser=?"


def test_where3():
    w = WhereClause("foo=?", "bar:n=    ?", "|eggs =  ?")
    assert str(w) == "WHERE foo='?' AND bar=? OR eggs='?'"


def test_where4():
    w = WhereClause("(foo=?", "bar=    '123')", "|eggs  =   \"balala\"")
    assert str(w) == "WHERE ( foo='?' AND bar='123' ) OR eggs='balala'"


def test_where5():
    w = WhereClause("foo=?", "(bar:n=    1.25", "|eggs:n=  30)")
    assert str(w) == "WHERE foo='?' AND ( bar=1.25 OR eggs=30 )"

##############################


def test_group1():
    g = GroupbyClause("mid")
    assert str(g) == "GROUP BY mid"


def test_group2():
    g = GroupbyClause("mid", "billid")
    assert str(g) == "GROUP BY mid, billid"


def test_group3():
    g = GroupbyClause('sorderid', 'pid', 'mid', having='faceprice > 3.5')
    assert str(g) == "GROUP BY sorderid, pid, mid HAVING faceprice > 3.5"

##############################


def test_order1():
    o = OrderbyClause("mid")
    assert str(o) == "ORDER BY mid"


def test_order2():
    o = OrderbyClause("addtime", "state")
    assert str(o) == "ORDER BY addtime, state"


def test_order3():
    o = OrderbyClause("-mid")
    assert str(o) == "ORDER BY mid DESC"


def test_order4():
    o = OrderbyClause('-sorderid', '+pid', '-addtime', 'mid')
    assert str(o) == "ORDER BY sorderid DESC, pid ASC, addtime DESC, mid"


def test_order5():
    o = OrderbyClause("+mid")
    assert str(o) == "ORDER BY mid ASC"

##############################


def test_delete0():
    d = Delete("t_system_orders", where="billid='S001'")
    assert str(d) == "DELETE FROM t_system_orders WHERE billid='S001'"


def test_delete1():
    d = Delete("t_system_orders", where=["billid='S001'", "|state:n   =   16"])
    assert str(
        d) == "DELETE FROM t_system_orders WHERE billid='S001' OR state=16"

##############################

def test_update0():
    u = Update(
        "t_system_orders",
        where=["billid='S001'", "(state:n  =   12", '|supuid is null)'],
        state='15',
        mid='A08566')
    assert str(
        u) == "UPDATE t_system_orders SET state = '15', mid = 'A08566' WHERE billid='S001' AND ( state=12 OR supuid is null )"

def test_update1():
    u = Update(
        "t_system_orders",
        where=["billid='S001'", "(supuid is null", '|state:n =         12)'],
        state='15',
        mid='A08566')
    assert str(
        u) == "UPDATE t_system_orders SET state = '15', mid = 'A08566' WHERE billid='S001' AND ( supuid is null OR state=12 )"

def test_update2():
    u = Update("t_system_orders", "billid='S001'", state='15')
    assert str(
        u) == "UPDATE t_system_orders SET state = '15' WHERE billid='S001'"


def test_update3():
    u = Update(
        "t_system_orders",
        ["billid='S001'", "|(state:n=12", '|supuid is null)'],
        state=15,
        mid='A08566')
    assert str(u) == "UPDATE t_system_orders SET state = '15', mid = 'A08566' WHERE billid='S001' OR ( state=12 OR supuid is null )"

def test_update4():
    u = Update(
        "t_system_orders",
        state='15',
        mid='A08566')
    assert str(
        u) == "UPDATE t_system_orders SET state = '15', mid = 'A08566'"

##############################

def test_insert0():
    insert = Insert("mb_config", id='1')
    assert str(insert) == "INSERT INTO mb_config ( id ) VALUES ( '1' )"

def test_insert1():
    insert = Insert("mb_config", id='1', mid='2', value='3')
    assert str(insert) == "INSERT INTO mb_config ( id, mid, value ) VALUES ( '1', '2', '3' )"


##############################

def test_select0():
    sel = Select()
    assert str(sel) == "SELECT *"

def test_select1():
    sel = Select("dual", fields='sysdate')
    assert str(sel) == "SELECT sysdate FROM dual"

def test_select2():
    sel = Select(fields=['sysdate', 'sysdate-1'], tables="dual")
    assert str(sel) == "SELECT sysdate, sysdate-1 FROM dual"

def test_select3():
    sel = Select("mb_config", where="mid='A08566'", fields=("id", "mid", "value"))
    assert str(sel) == "SELECT id, mid, value FROM mb_config WHERE mid='A08566'"

def test_select4():
    sel = Select(tables=['mb_config', 'mb_processlog'], where=["mid='A08566'", '|(state:n=13', "supuid='ofpay')"])
    assert str(sel) == "SELECT * FROM mb_config JOIN mb_processlog WHERE mid='A08566' OR ( state=13 AND supuid='ofpay' )"

def test_select5():
    sel = Select(tables=['mb_config', '<mb_processlog'], where=["mid='A08566'", '|(state:n =     13', "supuid='ofpay')"], group=('supuid', 'state', {'having':'price>13'}), order=['-addtime', 'state'])
    assert str(sel) == "SELECT * FROM mb_config LEFT JION mb_processlog WHERE mid='A08566' OR ( state=13 AND supuid='ofpay' ) GROUP BY supuid, state HAVING price>13 ORDER BY addtime DESC, state"

def test_select6():
    sel = Select(tables=('mb_config', '<mb_processlog', {'on': 's.id == sb.id'}), where=["mid='A08566'", '|(state:n=13', "supuid='ofpay')"], group=('supuid', 'state', {'having':'price>13'}), order=['-addtime', 'state'])
    assert str(sel) == "SELECT * FROM mb_config LEFT JION mb_processlog ON s.id == sb.id WHERE mid='A08566' OR ( state=13 AND supuid='ofpay' ) GROUP BY supuid, state HAVING price>13 ORDER BY addtime DESC, state"

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
