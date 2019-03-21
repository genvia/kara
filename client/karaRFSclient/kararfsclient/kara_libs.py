# -*- coding: utf-8 -*-

import sys
import os
import inspect
import string

from robot.libraries.BuiltIn import BuiltIn
from robot.api               import logger  as rfs_logger
from robot.api.deco          import keyword
from robot.api               import SuiteVisitor

import kara
from   kara.executor      import *
from   kara.database.util import *
from   kara.validator     import *

class KaraSetIdListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.rfs_buildin = BuiltIn()
        self.logged = False

    def library_import(self, name, attrs):
        if not self.logged and "KaraLibs" in name:
            client_id = kara.logging_client_running_id("RFS")
            self.rfs_buildin.set_global_variable("${KARA_CLIENT_ID}", client_id)
            # TODO: at the moment can not log to log file.
            # rfs_logger.info("Running Id: <b>{}</b>".format(client_id), html=True)
            print "Running Id: {}".format(client_id)
            self.logged = True


class TransactionCheck(SuiteVisitor):
    """
    检查用例事务的Setup / Teardown的一致性

    因为数据库是一开始就连接好，最后才断开，如果事务开启，提交/回滚不一致，将是灾难性的。
    所以实现一个Visitor，来检查一致性，在用例开始跑之前，检查事务的一致性
    """

    def __init__(self):
        self.rfs_buildin = BuiltIn()

    def start_test(self, test):
        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        setup    = test.keywords.setup
        teardown = test.keywords.teardown

        if setup and setup.name.encode("utf-8") == "数据库事务开启":
            if not teardown or teardown.name.encode("utf-8") not in ["数据库事务提交", "数据库事务回滚"]:
                self.rfs_buildin.fatal_error("\n\nTEST CASE\n<<<{}>>> HAS TRANSACTION SETUP, BUT NO FOUND TRANSACTION TEARDOWN, PLEASE CHECK IT.\n\n".format(str(test)))

    def end_test(self, test):
        pass


class KaraLibs(object):
    """
    基于kara的robot framework library，主要目的是为了简化基于robot frameowrk后台业务自动化的编写

    虽然robot framework提供了许多library，但因为它是通用测试框架，不可能有任何基于某种具体业务的library，
    也就是说没有相关业务的“胶水层”。而且提供的一些library使用起来也比较冗长。基于这些考虑，我们实现了一个
    通用的模块KARA，因为测试框架不光是robot framework一家，简而言之，KaraLibs只是KARA robot framework的一个客户端。
    """

    __version__ = '0.0.1'

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    DATABASE_TRANSACTION_VARIABLE_NAME = '@{__transactions__}'

    def __init__(self, *args, **kwargs):
        rfs_logger.debug("KaraLibs library importing...")
        self.rfs_buildin = BuiltIn()

    def __keyword_logging(self, msg_format_str, *args):
        """
        a help functin to logging robot framework.
        """

        caller_name = inspect.currentframe().f_back.f_code.co_name
        keyword_name = string.capwords(caller_name.replace('_', ' '))
        final_msg = "{}: {}: {}".format("[KaraLibs]", keyword_name, msg_format_str)
        rfs_logger.debug(final_msg.format(*args))

    @keyword(tags=["kara_libs"])
    def database_start_transaction(self, *db_names):
        """
        一个或多个数据库开启事务

        @Params: db_names: 数据库的名称，例如ofrc或main，同kara.cfg里配置
        """
        for name_str in db_names:
            if not name_str or not kara.opened_dbs[name_str]:
                raise ValueError("database [{}] has not opened!?".format(name_str))

        self.rfs_buildin.variable_should_not_exist(self.DATABASE_TRANSACTION_VARIABLE_NAME)

        transactions = [ kara.opened_dbs[name_str].begin() for name_str in db_names ]
        self.rfs_buildin.set_test_variable(self.DATABASE_TRANSACTION_VARIABLE_NAME, *transactions)
        self.__keyword_logging("started transaction: {}", self.rfs_buildin.get_variable_value(self.DATABASE_TRANSACTION_VARIABLE_NAME))

    @keyword(tags=["kara_libs"])
    def database_commit_transaction(self):
        """
        一个或多个数据库提交事务

        @Params: 没有参数，为了保证和事务开启的一致，特意牺牲了灵活，只会提交前面刚刚开启的那些全部的事务！
        """
        self.rfs_buildin.variable_should_exist(self.DATABASE_TRANSACTION_VARIABLE_NAME)

        [ trans.commit() for trans in self.rfs_buildin.get_variable_value(self.DATABASE_TRANSACTION_VARIABLE_NAME) ]
        self.__keyword_logging("committed transaction: {}", self.rfs_buildin.get_variable_value(self.DATABASE_TRANSACTION_VARIABLE_NAME))
        self.rfs_buildin.set_test_variable(self.DATABASE_TRANSACTION_VARIABLE_NAME, None)

    @keyword(tags=["kara_libs"])
    def database_rollback_transaction(self):
        """
        一个或多个数据库回滚事务

        @Params: 没有参数，为了保证和事务开启的一致，特意牺牲了灵活，只会回滚前面刚刚开启的那些全部的事务！
        """
        self.rfs_buildin.variable_should_exist(self.DATABASE_TRANSACTION_VARIABLE_NAME)

        [ trans.rollback() for trans in self.rfs_buildin.get_variable_value(self.DATABASE_TRANSACTION_VARIABLE_NAME) ]
        self.__keyword_logging("rollbacked transaction: {}", self.rfs_buildin.get_variable_value(self.DATABASE_TRANSACTION_VARIABLE_NAME))
        self.rfs_buildin.set_test_variable(self.DATABASE_TRANSACTION_VARIABLE_NAME, None)

    @keyword(tags=["kara_libs"])
    def opa_standard_make_order(self, order_type, fetch_billid = False, extra_params = None):
        """
        大接口标准版本下单，参数是订单的类型

        @Params: order_type
        HF_KC, HF_MC, HF_GH, LL, SUP_GAME, GAS_CARD, CARD_PASS, GGSHIYE
        @Params: fetch_bill: parse billid from response xml?
        @Params: extra_params: extra params sent
        @Return: a executor object
        """

        self.__keyword_logging("order type is [{}]", order_type)
        self.__keyword_logging("fetch bill is [{}]", fetch_billid)
        self.__keyword_logging("extra parameter is [{}]", extra_params)

        map = {'HF_KC':     ("onlineorder.do", "opa_std_hf.py"),
               'HF_MC':     ("onlineorder.do", "opa_std_hf_mc.py"),
               'HF_GH':     ("fixtelorder.do", "opa_std_hf_gh.py"),
               'HF_KD':     ("fixtelorder.do", "opa_std_hf_kd.py"),
               'LL':        ("flowOrder.do", "opa_std_ll.py"),
               'SUP_GAME':  ("onlineorder.do", "opa_std_game.py"),
               'GAS_CARD':  ("sinopec/onlineorder.do", "opa_std_gascard.py"),
               'CARD_PASS': ("order.do", "opa_std_cardpass.py"),
               'GGSHIYE':   ("utilityOrder.do", "opa_std_ggshiye.py"),
               'JINRONG':   ("transferAccounts.do", "opa_std_jinrong.py"),
               'GIFT':   ("gift/onlineorder.do", "opa_std_gift.py"),
               'GGSHIYECARD':   ("pubCard/pubCardOrder.do", "opa_std_ggshiyecard.py")
               }

        if not map[order_type]:
            raise ValueError("{}: order type parameters is invalidate.".format(order_type))

        self.__keyword_logging("opa interface is [{}]; params file is [{}]", map[order_type][0], map[order_type][1])

        opa_executor = OpaStdHTTPExecutor(map[order_type][0], map[order_type][1], fetch_billid, extra_params)
        opa_executor.invoke()
        return opa_executor

    @keyword(tags=["kara_libs"])
    def opa_standard_make_order_using_dict(self, interface_path, params_dict, stricted=True):
        """
        大接口标准版本下单，参数是一个Dictionary，而不是一个参数文件; 大接口的接口名也要传入

        @Params: interface_path: opa interface path
        @Params: params_dict: all http parameters
        @Return: opa executor object
        """

        self.__keyword_logging("opa interface is [{}]", interface_path)
        self.__keyword_logging("parameter dictionary is [{}]", params_dict)
        self.__keyword_logging("parameter stricted is [{}]", stricted)

        opa_executor = OpaStdSimpleHTTPExecutor(interface_path, params_dict, stricted)
        opa_executor.invoke()
        return opa_executor

    @keyword(tags=["kara_libs"])
    def opa_standard_batch_validate(self, obj, *conditions):
        """
        校验HTTP请求的响应或数据库字段的值

        @Params: obj: what to verify
        conditions: verify condition list
        @Return: True/False
        """

        self.__keyword_logging("validate target object is [{}]", obj)
        self.__keyword_logging("validate condition list are [{}]", conditions)

        return Validator.batch_verify(obj, *conditions)

    def __get_database_and_table_pre_db_handle(self, db_and_table):
        if '@' not in db_and_table:
            raise ValueError("database and table name parameter [{}] style is invalid, should be like 'ofrc@mb_config'.".format(db_and_table))

        tmp_array = db_and_table.split('@')
        db_name   = tmp_array[0]
        table     = tmp_array[1]
        if not db_name or not table:
            raise ValueError("database and table parameter [{}] is invalidate, should be like 'ofrc@mb_config'.".format(db_and_table))

        database = kara.opened_dbs[db_name]
        if not database or not database.connected:
            raise RuntimeError("WTF!? database {} dont connected.".format(db_name))

        return database, table

    @keyword(tags=["kara_libs"])
    def insert_into_database(self, db_and_table, **kwargs):
        """
        向数据库中插入记录

        @Params：db_and_table: database name and table name, split by '@'
        @Params: kwargs: dictionary of field and its value
        @Return: sqlalchemy result proxy object
        """

        self.__keyword_logging("db_and_table parameter is [{}]", db_and_table)
        self.__keyword_logging("insert values are [{}]", kwargs)

        database, table = self.__get_database_and_table_pre_db_handle(db_and_table)

        insert = str(Insert(table, **kwargs))
        self.__keyword_logging("Final insert sql is [{}]", insert)

        efforted = database.execute(insert)
        return efforted

    @keyword(tags=["kara_libs"])
    def delete_from_database(self, db_and_table, where_cond):
        """
        从数据库中删除记录

        @Params：db_and_table: database name and table name, split by '@'
        @Params: where_cond: where condition
        @Return: sqlalchemy result proxy object
        """

        self.__keyword_logging("db_and_table parameter is [{}]", db_and_table)
        self.__keyword_logging("where condition is [{}]", where_cond)

        database, table = self.__get_database_and_table_pre_db_handle(db_and_table)

        delete = str(Delete(table, where_cond))
        self.__keyword_logging("Final delete sql is [{}]", delete)

        efforted = database.execute(delete)
        return efforted

    @keyword(tags=["kara_libs"])
    def update_in_database(self, db_and_table, where_cond=None, **kwargs):
        """
        在数据库中更新记录

        @Params：db_and_table: database name and table name, split by '@'
        @Params: where_cond: optional where condition
        @Params: kwargs: dictionary of field and values
        @Return: sqlalchemy result proxy object
        """

        self.__keyword_logging("db_and_table parameter is [{}]", db_and_table)
        self.__keyword_logging("where condition is [{}]", where_cond)
        self.__keyword_logging("parameter dictionary is [{}]", kwargs)

        database, table = self.__get_database_and_table_pre_db_handle(db_and_table)

        update = str(Update(table, where_cond, **kwargs))
        self.__keyword_logging("Final update sql is [{}]", update)

        efforted = database.execute(update)
        return efforted

    @keyword(tags=["kara_libs"])
    def execute_single_sql_statement(self, db_name, sql_str, **kwargs):
        """
        在数据库中单独执行一个预编译形式（可以带参数）的SQL语句

        如果karaLibs提供的增删改查不满足需要，或者不方便，可以用此方法执行原始的 SQL语句
        @Params：db_name: database name,  example: ofrg, or main
        @Params: sql_str: in turn: sql statement
        @Params: kwargs: in turn: optional prepared statement parameters dictionary
        @Return: sqlalchemy result proxy object
        """

        self.__keyword_logging("database name is [{}]", db_name)
        self.__keyword_logging("sql statement is [{}]", sql_str)
        if kwargs:
            self.__keyword_logging("sql statement parameters are [{}]", kwargs)

        database = kara.opened_dbs[db_name]
        if not database or not database.connected:
            raise RuntimeError("WTF!? database {} dont connected.".format(db_name))

        result = database.execute(sql_str, **kwargs)
        return result

    @keyword(tags=["kara_libs"])
    def execute_sql_file(self, db_name, sql_file, **kwargs):
        """
        在数据库中一个事务内执行sql文件（可以带参数）

        如果karaLibs提供的增删改查不满足需要，或者不方便，可以用此方法执行原始的 SQL 文件
        @Params：db_name: database name,  example: ofrg, or main
        @Params: sql_file: sql file name
        @Params: kwargs: in turn: optional prepared statement parameters dictionary
        @Return: sqlalchemy result proxy object
        """

        self.__keyword_logging("database name is [{}]", db_name)
        self.__keyword_logging("sql file name is [{}]", sql_file)
        if kwargs:
            self.__keyword_logging("sql statement parameters are [{}]", kwargs)

        database = kara.opened_dbs[db_name]
        if not database or not database.connected:
            raise RuntimeError("WTF!? database {} dont connected.".format(db_name))

        absulte_path = os.path.join(kara.KARA_HOME, kara.SQL_FILE_DIR, sql_file)
        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        self.__keyword_logging("final sql file absult path is [{}]", absulte_path)
        result = database.execute_sql_file(absulte_path, **kwargs)
        return result

    def __fetch_from_database_single_table(self, db_and_table, fetchall, *where_and_others):
        self.__keyword_logging("db_and_table parameter is [{}]", db_and_table)
        self.__keyword_logging("where_and_other is [{}]", where_and_others)

        database, table = self.__get_database_and_table_pre_db_handle(db_and_table)

        select = str(Select(table, *where_and_others))
        self.__keyword_logging("Final select sql is [{}]", select)

        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        record = database.fetch(select, fetchall)
        return record

    @keyword(tags=["kara_libs"])
    def fetch_from_database_single_table(self, db_and_table, *where_and_others):
        """
        从数据库中查询单条记录

        @Params：db_and_table: database name and table name, split by '@'
        @Params: where_and_others: in turn: where, fields, group by , order by...
        @Return: KaraCursor object or KaraCursorSet object
        """
        return self.__fetch_from_database_single_table(db_and_table, False, *where_and_others)


    @keyword(tags=["kara_libs"])
    def fetch_multi_from_database_single_table(self, db_and_table, *where_and_others):
        """
        从数据库中查询多条记录

        @Params：db_and_table: database name and table name, split by '@'
        @Params: where_and_others: in turn: where, fields, group by , order by...
        @Return: KaraCursor object or KaraCursorSet object
        """
        return self.__fetch_from_database_single_table(db_and_table, True, *where_and_others)


    @keyword(tags=["kara_libs"])
    def ofrg_fetch_order(self, supuid, num):
        """
        充值中心供货商取单

        @Params: supuid: supuid
        @Params: num   : how many order will get
        @Return: ofrg fetch executor object
        """
        self.__keyword_logging("ofrg fetch parameters are [{}, {}]", supuid, num)

        ofrg_fetch = OfrgFetchOrderHTTPExecutor(kara.conf.uts.ofrg.host)
        payload           = dict()
        payload['supUid'] = supuid
        payload['num']    = num
        ofrg_fetch.invoke(payload)

        self.__keyword_logging("ofrg fetched orders num is [{}]", ofrg_fetch.count)
        return ofrg_fetch

# TODO
    def __ofrg_callback_order(self, supuid, billid, callback_type):
        """
        a help functin to callback order in ofrg.
        """
        self.__keyword_logging("ofrg callback order parameters are [{}, {}, {}]", supuid, billid, callback_type)

        ofrg_callback = OfrgCallbackHTTPExecutor(kara.conf.uts.ofrg.host, callback_type)
        payload            = dict()
        payload['supuid']  = supuid
        payload['orderid'] = billid
        ofrg_callback.invoke(payload)

        self.__keyword_logging("ofrg callback orders result is [{}]", ofrg_callback.resp_text)
        return ofrg_callback

    @keyword(tags=["kara_libs"])
    def ofrg_callback_order(self, supuid, billid, callback_type):
        """
        充值中心供货商回调订单

        @Params: supuid:        supuid
        @Params: billid:        which order to be callback
        @Params: callback_type: callback type

        @Return: ofrg callback executor object
        """
        return self.__ofrg_callback_order(supuid, billid, callback_type)

    @keyword(tags=["kara_libs"])
    def kernel_make_order(self, params_dict):
        """
        帐务下单，参数是字典，key是path，templeate_file

        @Params: params_dict
            path: 请求的http url path
            file: 参数文件或者从robot framework的变量文件中得到的json对象
        @Return: kernel executor object
        """

        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        self.__keyword_logging("kernel order interface is [{}]; params file is [{}]", params_dict['path'], params_dict['file'])
        kernel_executor = KernelNormalHTTPExecutor(params_dict['path'], params_dict['file'])
        kernel_executor.invoke()
        return kernel_executor

    @keyword(tags=["kara_libs"])
    def kernel_make_callback(self, params_dict):
        """
        帐务回调，参数是字典，key是path，templeate_file

        @Params: params_dict
            path: 请求的http url path
            file: 参数文件或者从robot framework的变量文件中得到的json对象
        @Return: kernel executor object
        """

        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        self.__keyword_logging("kernel callback interface is [{}]; params file is [{}]", params_dict['path'], params_dict['file'])
        kernel_executor = KernelCallbackHTTPExecutor(params_dict['path'], params_dict['file'])
        kernel_executor.invoke()
        return kernel_executor

if __name__ == "__main__":
    # opa = KaraLibs().opa_standard_make_order('HF_KC')
    # rec = KaraLibs().fetch_from_database_single_table("ofrc@mb_config", "mid=NEWCALLBACK")
    # fetch = KaraLibs().ofrg_fetch_order('yczc006', 100)
    # cb = KaraLibs().ofrg_callback_order('yczc006', "S001", "cancelOrder")
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

