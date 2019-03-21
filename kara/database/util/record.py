# -*- coding: utf-8 -*-

import os

from collections import OrderedDict

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

import kara

class Database(object):
    def __init__(self, url=None, **kwargs):
        self.url = url
        if not self.url:
            raise ValueError("must give me a database url.")

        self.db           = create_engine(self.url, **kwargs).connect()
        self.connected    = True
        self.__tablenames = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.close()

    def close(self):
        if self.connected:
            self.db.close()
            self.connected = False

    def begin(self):
        if self.connected:
            return self.db.begin()

    def table_names(self, refresh=False):
        if not self.connected:
            raise ValueError("database has not connected.")
        if not self.__tablenames or refresh:
            meta = declarative_base().metadata
            meta.reflect(self.db)
            self.__tablenames = meta.tables.keys()

        return self.__tablenames

    def fetch(self, querystr, fetchall=False, **params):
        if not self.connected:
            raise ValueError("database has not connected.")
        cursor = self.db.execute(text(querystr), **params)
        allrecords_genertor = (KaraCursor(cursor.keys(), row) for row in cursor)
        try:
            result_obj = KaraCursorSet(allrecords_genertor) if fetchall else allrecords_genertor.next()
        except StopIteration:
            result_obj = None

        return result_obj

    def execute(self, sqlstr, **params):
        if not self.connected:
            raise ValueError("database has not connected.")
        result = self.db.execute(text(sqlstr), **params)
        return result

    def execute_sql_file(self, absulte_path, **params):
        """
        execute one sql file in a transaction

        if all sql statement are execute success, will return one dictionary of sql statement and its effect rowcount pair

        SQL file for kara Database object require:
          1. one sql statement must completely be in one line.
          2. can comment use '--' or '#', but have to comment at first column
          3. ';' at end of one line is optional.
          4. empty line is ignored.
          5. file encoding must be utf-8

          example:
            # change ofrc@t_sys_orders orders state
            UPDATE t_sys_orders SET state=13 WHERE addtime>trunc(sysdate,'dd')

            -- change ofrc@t_sys_orders orders state
            UPDATE t_recharge_order SET state=13 WHERE addtime>trunc(sysdate,'dd');
        """
        if not os.path.isfile(absulte_path):
            raise ValueError("sql file [{}] not found.".format(absulte_path))
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        # import pudb; pudb.set_trace()  # XXX BREAKPOINT
        result=dict()
        with open(absulte_path, 'r') as f:
            with self.begin():
                for sql_line in filter(lambda x: not x.startswith("--") and not x.startswith('#') and x.replace(';', '').strip(), f):
                    sql = sql_line.replace(";", '').strip()
                    result_proxy_obj = self.db.execute(text(sql), **params)
                    result[sql] = result_proxy_obj.rowcount
        return result


class KaraCursor(object):
    __slots__ = ("_keys", "_values")

    def __init__(self, keys, values):
        if len(keys) != len(values):
            raise ValueError("length do not equal between keys and values.")
        self._keys = keys
        self._values = values

    def __len__(self):
        return 1

    @property
    def keys(self):
        return self._keys

    @property
    def values(self):
        return self._values

    def __getitem__(self, who):
        # do not support slice object
        if isinstance(who, int):
            if who not in xrange(len(self.keys)):
                raise ValueError("index out of keys.")
            return self.values[who]

        if who in self.keys:
            index = self.keys.index(who)
            return self.values[index]

        raise KeyError("KaraCursor cantain no '{}'".format(who))

    def __getattr__(self, attrname):
        try:
            return self[attrname]
        except KeyError as e:
            raise AttributeError(e)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def as_dict(self, ordered=False):
        items = zip(self.keys, self.values)
        return OrderedDict(items) if ordered else dict(items)

    def as_obj(self):
        obj = type('', (), {})
        for i in xrange(len(self.keys)):
            setattr(obj, self.keys[i], self.values[i])
        return obj


class KaraCursorSet(object):
    def __init__(self, generator, maxsizelimit=50):
        self._generator = generator
        self._all_rows = []
        self._maxsize = maxsizelimit
        self.eof = False

    def __len__(self):
        return len(self._all_rows)

    def __getitem__(self, index):
        # do not support slice object
        # because has __iter__ method, so only for x[i] .
        if not isinstance(index, int):
            raise ValueError("index is not valid index for KaraCursorSet.")
        if index not in xrange(len(self._all_rows)):
            raise IndexError("index out of limit.")
        return self._all_rows[index]

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            next_row = next(self._generator)
            self._all_rows.append(next_row)
            return next_row
        except StopIteration:
            self.eof = True
            raise StopIteration("KaraCursorSet no more record.")

    def __iter__(self):
        # this function is a generator, gnerator always is a iter object
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                if i >= self._maxsize:
                    self.eof = True
                    raise StopIteration()
                yield self.next()
            i += 1


if __name__ == "__main__":
    def gensequence(n):
        for i in xrange(n):
            yield i

    k = KaraCursorSet(gensequence(10), 5)
    k.next()
    k.next()
    k.next()
    print k._all_rows
    print "=============================="
    print k[0]
    for i in k:
        print i
    print "=============================="
    print k[4]
    # print k[5]

    # url = "oracle://ofrc:ofcard@172.19.100.223:1521/oncz"
    # with Database(url, echo=False) as ofrc:
    #     record = ofrc.fetch("select * from mb_config")
    #     print type(record)
    #     obj = record.as_obj()
    #     print obj.mid
    #     print obj.key
    #     print obj.value
    #     print "=============================="
    #     record = ofrc.fetch("select * from mb_config", True)
    #     print type(record)
    #     print len(record)
    #     for i in record:
    #         obj = i.as_obj()
    #         print obj.mid + ": " + obj.value
    #     print len(record)

    print "=============================="
        # record = ofrc.fetch(
        #     "select * from mb_config where mid='ACCOUNTLIMITNUMBER'")
        # d = record.as_dict()
        # print d['value']
        # print "=============================="
        # record = ofrc.fetch(
        #     "select * from t_sys_orders where outorderid='S1610238680842'")
        # obj = record.as_obj()
        # print obj.add_m_no
        # print obj.supuid
        # print "=============================="

        # import kara
        # from kara.database.util.sqlbuilder import Select
        # sel = Select(
        #     tables="t_sys_orders", where=["outorderid='S1610238680842'"])
        # print sel
        # record = ofrc.fetch(str(sel))
        # obj = record.as_obj()
        # print obj.add_m_no, obj.state
        # print obj.support_supuids

        # print "=============================="
        # sel = Select(
        #     tables='t_sys_orders',
        #     where=["add_m_no='A923501'", 'state=13'],
        #     order=['-addtime', 'state'])
        # print sel
        # record = ofrc.fetch(str(sel))
        # obj = record.as_obj()
        # print record.keys
        # print record.values
        # print obj.product_no

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
