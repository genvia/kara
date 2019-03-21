# -*- coding: utf-8 -*-

import string
import uuid
import random
# from argparse import Namespace

# TODO: why not run in pytest where used relatived impport
# from . import common_params
# from kara.executor.params import common_params
import kara

################################################################################
# 此前的语句不要修改
################################################################################

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

vars = dict()
vars["saleOrderId"] = str(uuid.uuid1())
vars["userCode"]    = random.choice(["A08566", "A923360"])
vars["outOrderId"]  = str(uuid.uuid1())

################################################################################
# 此后的语句不要修改
################################################################################

# TODO：why occure error: global name 'argparse' is not defined
# template_data_json=json.loads(template.substitute(vars), object_hook=lambda d: argparse.Namespace(**d))

template_str = template.substitute(vars)

del string
del uuid
del random
# del argparse

del kara

del template
del vars

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
