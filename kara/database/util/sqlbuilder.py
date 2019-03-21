# -*- coding: utf-8 -*-

import re


class ClauseBase(object):
    def __init__(self, *fregments, **options):
        self.orign_fregemnts = fregments
        # self.fregments = list(fregments)

        self.fregments = self.__normalize_fregment(fregments)
        self.options = options

        if self.options and self.option_key not in self.options:
            raise ValueError(self.__class__.__name__ + ": " +
                             "option is invalid.")

        if not self.fregments:
            raise ValueError(self.__class__.__name__ + ": " +
                             "parameter is empty.")
        for element in self.fregments:
            if not element:
                raise ValueError(self.__class__.__name__ + ": " +
                                 "parameter element is empty.")

    def __normalize_fregment(self, fregments):
        result = []
        for index, element in enumerate(fregments):
            # only contains '=' will be normalized.
            has_parenthese = False
            if element.find('=') > 0:
                el = re.sub(r"\s*=\s*['\"]?", "=", element)
                el = el.rstrip(' ')

                # handle maybe existed ')'
                if el.endswith(')'):
                    el = el.rstrip(')')
                    el = el.rstrip("\"'")
                    has_parenthese = True
                else:
                    el = el.rstrip("\"'")

                if el.find(":n") <= 0:
                    el = re.sub(r"=(.*)", r"='\1'", el)
                else:
                    el = el.replace(":n", '')

                if has_parenthese:
                    el += ')'
            else:
                el = element
            result.append(el)

        return result

    def pre_to_string(self):
        pass

    def to_string_internal(self):
        return ""

    def post_to_string(self, draft_result_string):
        tmp = re.sub(r"\s+", " ", draft_result_string)
        tmp = re.sub(r"\s*,\s*", ", ", tmp)
        return tmp.strip()

    def to_string(self):
        self.pre_to_string()
        return self.post_to_string(self.to_string_internal())

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        extra_str = self.options if self.options else '{}'
        return "{} | PARAS: {} | OPTION: {}".format(
            self.__class__.__name__, self.orign_fregemnts, extra_str)


class FromClause(ClauseBase):
    keyword = " FROM "
    extra_keyword = " ON "
    join_symbol = {'<': " LEFT JION ", '>': " RIGHT JION ", '#': " JOIN "}
    option_key = extra_keyword.lower().strip()

    def pre_to_string(self):
        if len(self.fregments) == 2:
            for index, part in enumerate(self.fregments[1:]):
                if part[0] in self.join_symbol.keys():
                    self.fregments[index + 1] = part.replace(
                        part[0], self.join_symbol[part[0]], 1)
                else:
                    self.fregments[index + 1] = self.join_symbol['#'] + part

    def to_string_internal(self):
        extra_part = self.extra_keyword + self.options.get(
            self.extra_keyword.lower().strip(), "") if self.options else ""
        return self.keyword + " ".join(self.fregments) + extra_part


class WhereClause(ClauseBase):
    keyword = " WHERE "
    group_symbol = {'(': " ( ", ')': " ) "}
    operator_symbol = {'&': " AND ", '|': " OR "}

    def pre_to_string(self):
        for index, part in enumerate(self.fregments):
            for k, v in self.group_symbol.items():
                if k in part:
                    self.fregments[index] = part.replace(k, v, 1)

        if len(self.fregments) > 1:
            for index, part in enumerate(self.fregments[1:]):
                if part[0] == '|':
                    self.fregments[index + 1] = part.replace(
                        part[0], self.operator_symbol[part[0]], 1)
                else:
                    self.fregments[index + 1] = self.operator_symbol[
                        '&'] + part

    def to_string_internal(self):
        return self.keyword + ' '.join(self.fregments)


class OrderbyClause(ClauseBase):
    keyword = " ORDER BY "
    order_sysmol = {'-': " DESC ", '+': " ASC "}

    def pre_to_string(self):
        for index, part in enumerate(self.fregments):
            for k, v in self.order_sysmol.items():
                if k in part:
                    self.fregments[index] = re.sub(
                        r"(\w+)\s+(\w+)", r" \2 \1 ", part.replace(k, v, 1))

    def to_string_internal(self):
        return self.keyword + ",".join(self.fregments)


class GroupbyClause(ClauseBase):
    keyword = " GROUP BY "
    extra_keyword = " HAVING "
    option_key = extra_keyword.lower().strip()

    def to_string_internal(self):
        extra_part = self.extra_keyword + self.options.get(
            self.extra_keyword.lower().strip(), "") if self.options else ""
        return self.keyword + ",".join(self.fregments) + extra_part


class SqlStatement(object):
    def get_list(self, val):
        if not val:
            return []
        elif not hasattr(val, "__iter__") or isinstance(val, basestring):
            return [val]
        else:
            return list(val)

    def get_sub_clause(self, val, clause_cls):
        if val is None:
            return clause_cls()
        elif hasattr(val, "get"):
            return clause_cls(**val)
        elif hasattr(val, "__iter__"):
            # from has on, group has having.
            # dict must be the last one.
            if isinstance(val[-1], dict):
                return clause_cls(*val[:-1], **val[-1])
            else:
                return clause_cls(*val)
        else:
            return clause_cls(val)

    # def split_mixed_params(self, mixed):
    #     result = [[],{}]
    #     if isinstance(mixed, tuple) or isinstance(mixed, list):
    #         for element in mixed:
    #             if hasattr(element, "get"):
    #                 # only support one dict in list!
    #                 result[1] = element.copy()
    #             else:
    #                 result[0].append(element)

    #     return tuple(result)


class Delete(SqlStatement):
    def __init__(self, table, where=None):
        self.table = table
        self.where = where

    def __str__(self):
        sql = 'DELETE FROM {}'.format(self.table)
        if self.where:
            sql += ' {}'.format(self.get_sub_clause(self.where, WhereClause))
        return sql


class Update(SqlStatement):
    def __init__(self, table, where=None, **kwargs):
        self.table = table
        self.set_params = kwargs
        self.where = where

    def __str__(self):
        sql = 'UPDATE {} SET '.format(self.table)
        sql += ', '.join(("{} = '{}'".format(col, p)
                          for col, p in self.set_params.items()))
        if self.where:
            sql += ' {}'.format(self.get_sub_clause(self.where, WhereClause))
        return sql

class Insert(SqlStatement):
    def __init__(self, table, **kwargs):
        self.table = table
        self.insert_params = kwargs
        if not self.insert_params:
            raise ValueError(self.__class__.__name__ + ": " + "insert values dictionary must be here.")

    def __str__(self):
        sql = "{} {}".format("INSERT INTO", self.table)
        kstr = vstr = " ( "
        sorted_keys = self.insert_params.keys()
        sorted_keys.sort()
        for k in sorted_keys:
            kstr += "" + str(k) + ", "
            current_value = str(self.insert_params[k])
            if current_value.endswith(":n"):
                vstr += current_value.replace(":n", "") + ", "
            else:
                vstr += "'" + current_value + "'" + ", "
        kstr = kstr.rstrip().rstrip(",") + " )"
        vstr = vstr.rstrip().rstrip(",") + " )"

        sql += kstr + " VALUES" + vstr
        return sql

# USE MAP IS PREFECT.

# class Insert(SqlStatement):
#     def __init__(self, table, vals=None, cols=None):
#         self.table = table
#         self.vals = vals
#         self.cols = cols
#         if not vals:
#             raise ValueError(self.__class__.__name__ + ": " + "vals must be here.")

#     def __get_fields_list_str(self, vals):
#         if hasattr(vals, "__iter__"):
#             return "({})".format(", ".join(vals))
#         if vals.startswith('(') and vals.endswith(')'):
#             return vals
#         return "({})".format(vals)

#     def __str__(self):
#         sql = "{} {}".format("INSERT INTO", self.table)
#         if self.cols:
#             sql += " {}".format(self.__get_fields_list_str(self.cols))
#         sql += " VALUES {}".format(self.__get_fields_list_str(self.vals))
#         return sql


class Select(SqlStatement):
    def __init__(self, tables=None, where=None, fields=None, group=None, order=None):
        self.fields = fields if fields is not None else ['*']
        self.tables = tables
        self.where  = where
        self.group  = group
        self.order  = order

    def __str__(self):
        sql  = 'SELECT '
        sql += ", ".join(self.get_list(self.fields))
        if self.tables:
            sql += " {}".format(self.get_sub_clause(self.tables, FromClause))
        if self.where:
            sql += " {}".format(self.get_sub_clause(self.where, WhereClause))
        if self.group:
            sql += " {}".format(self.get_sub_clause(self.group, GroupbyClause))
        if self.order:
            sql += " {}".format(self.get_sub_clause(self.order, OrderbyClause))

        return sql


if __name__ == "__main__":
    # sel = Select()
    # print sel
    # sel = Select('sysdate', "dual")
    # print sel
    # sel = Select(fields=['sysdate', 'sysdate-1'], tables="dual")
    # print sel
    # sel = Select(tables="mb_config", where="mid='A08566'")
    # print sel
    # sel = Select(tables=['mb_config', 'mb_processlog'], where=["mid='A08566'", '|(state=13', "supuid='ofpay')"])
    # print sel
    # sel = Select(tables=['mb_config', '<mb_processlog'], where=["mid='A08566'", '|(state=13', "supuid='ofpay')"], group=('supuid', 'state', {'having':'price>13'}), order=['-addtime', 'state'])
    # print sel
    # sel = Select(tables=('mb_config', '<mb_processlog', {'on': 's.id == sb.id'}), where=["mid='A08566'", '|(state=13', "supuid='ofpay')"], group=('supuid', 'state', {'having':'price>13'}), order=['-addtime', 'state'])
    # print sel
    # insert = Insert("mb_config", vals=['?','?','?'], cols=['id', 'mid', 'value'])
    # print insert
    # insert = Insert("mb_config", vals=['?','?','?'])
    # print insert
    # # d = Delete("t_system_orders", where="billid='S001'")
    # print d
    # d = Delete("t_system_orders", where=["billid='S001'", "|state='16'"])
    # print d
    # u = Update("t_system_orders", state='15')
    # print u
    # u = Update("t_system_orders", where="billid='S001'", state='15')
    # print u
    # u = Update( "t_system_orders", where=["billid='S001'", "(state=12", '|supuid is null)'], state='15', mid='A08566')
    # print u
    # print "------------------------------"

    # def real_delete(table, where):
    #     d = Delete(table, where)
    #     print d

    # real_delete("saleuser", where="usercode == 'A001'")
    # real_delete("saleuser", where=["usercode == 'A001'", "state=1"])
    # print "------------------------------"

    # def real_update(table, where, **kwargs):
    #     print locals()
    #     d = Update(table, where, **kwargs)
    #     print d

    # # real_update( "t_system_orders", where="billid='S001'", state='15', mid='A08566')
    # real_update( "t_system_orders", where=["billid='S001'", "|(state=12", '|supuid is null)'], state='15', mid='A08566')

    pass


# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
