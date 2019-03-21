# -*- coding: utf-8 -*-

"""
帐务的Olp下单参数文件
"""

import uuid
import json
import argparse
import string

from robot.libraries.BuiltIn import BuiltIn as _rfs_builtin
from robot.api               import logger  as _rfs_logger

# import kara    as _kara

def get_variables(vars_type=None):
    def from_template_data_to_json(var):
        ################################################################################
        # 只能修改此块，其它最好不要动
        template = string.Template("""
        {
        "payMethod": {
            "payBankCode": "支付银行编号1",
            "payBankName": "支付银行名称1",
            "payGateCode": "ZDY_ALIPAY_WAP",
            "payGateName": "支付宝PC"
        },
        "payRequest": {
            "cateId": "10401",
            "cateName": "话费快充",
            "domainType": "23",
            "itemId": "111",
            "itemName": "河南联通手机快充10元",
            "orderCash": 1000.123,
            "payIp": "127.0.0.1",
            "payUserCode": "A85559911",
            "saleOrderId": "${saleOrderId}",
            "userAgent": "lalalalala",
            "userCode": "${userCode}",
            "remark": "string",
            "extendParams": {"abc":"123","abd":"123"},
            "outOrderId": "${outOrderId}"
        }
        }
        """)
        ################################################################################

        json_data = json.loads(template.substitute(var))
        return json_data

    def get_kernel_normal_make_order_dict(userid):
        d = dict()
        ################################################################################
        # 只能修改此块，其它最好不要动
        d['path']       = "pay/paymentOlp"

        vars = dict()
        vars["userCode"]    = userid
        vars["saleOrderId"] = str(uuid.uuid1())
        vars["outOrderId"]  = str(uuid.uuid1())
        ################################################################################
        d['file'] = from_template_data_to_json(vars)

        return d

    variables = {
        # 商户被锁定
        'OLP_USER_LOCKED':                   get_kernel_normal_make_order_dict('A08566'),
    }
    return variables

if __name__ == "__main__":
    vars = get_variables()
    import pprint as pp
    pp.pprint(vars)

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

