# -*- coding: utf-8 -*-

"""
帐务的支持自定义个别值的下单参数文件
"""

import uuid
import json
import argparse
import string

from robot.libraries.BuiltIn import BuiltIn as _rfs_builtin
from robot.api               import logger  as _rfs_logger

# import kara    as _kara

class KernelCustomizeVariables(object):
    def __init__(self, path, extra_param = None):
        self.path        = path
        self.extra_param = extra_param if not extra_param else {}

    def _get_params_json(self, var):
        ################################################################################
        # 只能修改此块，其它最好不要动

        template = string.Template("""
        {
        "payMethod": {
            "payBankCode": "1",
            "payBankName": "1",
            "payGateCode": "ZDY_ALIPAY_WAP",
            "payGateName": "PC"
        },
        "payRequest": {
            "cateId": "10401",
            "cateName": "4",
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
        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT

        json_data = json.loads(template.substitute(var))
        return json_data

    def fetch(self):
        _rfs_logger.debug("Kernel Customize Variables got extra parameters is %s" % self.extra_param)
        if not isinstance(self.extra_param, dict):
            raise RuntimeError("extra params must be dictionary.")

        # all string litera in robot framework is unicode! but string template only support string!
        # must convert it!
        for (k, v) in self.extra_param.items():
            if isinstance(v, unicode):
                self.extra_param[k] = str(v)

        d = dict()
        ################################################################################
        # 只能修改此块，其它最好不要动
        d['path'] = self.path

        vars = dict()
        vars["userCode"]    = 'A08566'
        vars["saleOrderId"] = str(uuid.uuid1())
        vars["outOrderId"]  = str(uuid.uuid1())

        vars.update(self.extra_param)
        ################################################################################
        d['file'] = self._get_params_json(vars)

        return d

################################################################################
# 只能修改此块，其它最好不要动
# 这里定义一些需要自定义的下单接口，只要是用这样的形式的，都需要在此定义

def get_variables():
    variables = {
                 "KERNEL_CUSTOMIZED_VARIABLES_OLP": KernelCustomizeVariables("pay/paymentOlp"),
                }
    return variables

################################################################################

if __name__ == "__main__":
    vars = dict()
    vars["userCode"]    = "A987654"
    vars["saleOrderId"] = str(uuid.uuid1())
    vars["outOrderId"]  = str(uuid.uuid1())

    import pprint as pp
    pp.pprint(KERNEL_CUSTOMIZED_VARIABLES_OLP.fetch(vars))

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

