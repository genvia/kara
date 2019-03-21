# -*- coding: utf-8 -*-

"""
大接口标准版本的一些特殊商户下单参数文件

因为在kara中，大接口的executor下单有两种方式，一种是文件，一种是参数Dictionary，
但是Dictionary全写在用例文件中一来太烦，二来还要计算md5，
所以考虑用variable file的方式
"""

import time    as _time
import uuid    as _uuid
import random  as _random
import hashlib as _hashlib

from robot.libraries.BuiltIn import BuiltIn as _rfs_builtin
from robot.api               import logger  as _rfs_logger

import kara    as _kara

# 下单时帐务相关的商户
# 'A923501' ~ 'A923503' 正常下单用它们三个，都是只有后付费的
# 'A923504' 商户被锁定
# 'A923505' 商户被废弃
# 'A923506' 预付费，没有任何类目的下单权限
# 'A923507' 能下单，预付费，余额不足
# 'A923508' 能下单，预付费, 余额充足
# 'A923509' 同时有信用点和预付费，却都没有任何类目的下单权限
# 'A923510' 信用点和后付费都有，信用点优先，但没余额
# 'A923511' 信用点和后付费都有，信用点优先，信用点余额充足
# 'A923512' 信用点和后付费都有，后付费优先，虽然信用点余额充足

def get_variables(vars_type=None):
    def get_opa_special_user_make_hf_order_dict(userid):
        d = dict()
        d['userid']       = userid
        # TODO
        good_user = ['A923508', 'A923510', 'A923511', 'A923512']
        # 固定为 内蒙古电信手机快充1元
        if d['userid'] in good_user:
            d['game_userid'] = '1532600' + str(_random.randint(1, 9999)).zfill(4)
        else:
            d['game_userid']  = _random.choice(_kara.conf.params.opa.hf_prefix) + str(_random.randint(1, 9999)).zfill(4)

        d['sporder_id']   = str(_uuid.uuid1())
        d['sporder_time'] = _time.strftime("%Y%m%d%H%M%S", _time.localtime())
        d['cardid']       = '140000'
        d['cardnum']      = '1'

        d['userpws'] = _kara.conf.params.opa.userpwd
        d['ret_url'] = _kara.conf.params.opa.callback_url
        d['version'] = _kara.conf.params.opa.version
        d['md5_key'] = _kara.conf.params.opa.md5_key

        md5obj  = _hashlib.md5()
        md5obj.update(d['userid'] + d['userpws'] + d['cardid'] + d['cardnum'] + d['sporder_id'] + d['sporder_time'] + d['game_userid'] + d['md5_key'])
        d['md5_str'] = md5obj.hexdigest().upper()

        return d

    variables = {
        # 商户被锁定
        'OPA_PARAMS_USER_LOCKED':                   get_opa_special_user_make_hf_order_dict('A923504'),
        # 商户被废弃
        'OPA_PARAMS_USER_DISCARD':                  get_opa_special_user_make_hf_order_dict('A923505'),
        # 在帐务侧没有任何类目下单权限的商户
        'OPA_PARAMS_USER_CATEGORY_LIMITED':         get_opa_special_user_make_hf_order_dict('A923506'),
        # 用户状态均正常，预付费，余额不足
        'OPA_PARAMS_USER_BALANCE_IS_ZERO':          get_opa_special_user_make_hf_order_dict('A923507'),
        # 仅有信用点帐号，也有类目下单权限，余额充足
        'OPA_PARAMS_USER_ONLY_XYD_ENGOUGH':         get_opa_special_user_make_hf_order_dict('A923508'),
        # 同时有信用点和预付费，却都没有任何类目的下单权限
        'OPA_PARAMS_USER_ALL_CATEGORY_LIMITED':     get_opa_special_user_make_hf_order_dict('A923509'),
        # 信用点和后付费都有，信用点优先，但没余额
        'OPA_PARAMS_USER_ALL_XYD_IS_ZERO_USE_HFF':  get_opa_special_user_make_hf_order_dict('A923510'),
        # 信用点和后付费都有，信用点优先，信用点余额充足
        'OPA_PARAMS_USER_ALL_XYD_ENGOUGH_USE_XYD':  get_opa_special_user_make_hf_order_dict('A923511'),
        # 信用点和后付费都有，后付费优先，虽然信用点余额充足
        'OPA_PARAMS_USER_ALL_HFF_IS_FIRST_USE_HFF': get_opa_special_user_make_hf_order_dict('A923512')
    }
    return variables

if __name__ == "__main__":
    vars = get_variables()
    import pprint as pp
    pp.pprint(vars)

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

