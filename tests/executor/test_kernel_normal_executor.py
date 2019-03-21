# -*- coding: utf-8 -*-

from pprint import pprint as pp

import kara
from kara.executor import *
from kara.database.util import *
from kara.validator import *


class TestKernelNormalHTTPExecutor(object):
    def test_kernel_normal_payment_std_executor_using_file(self):
        kernel_executor = KernelNormalHTTPExecutor("pay/paymentOlp", "kernel_pay_olp.template.py")
        # import pudb; pudb.set_trace()  # XXX BREAKPOINT
        result = kernel_executor.invoke()
        assert result.status_code == 200
        # pp(kernel_executor.raw)
        # pp(kernel_executor.raw['resp_json'])
        # pp(kernel_executor.resp_json.data.olpOrderDomain.userCode)
        # pp(kernel_executor.resp_json.data.olpOrderDomain.saleSysOrderId)
        assert kernel_executor.userCode == kernel_executor.resp_json.data.olpOrderDomain.userCode
        assert kernel_executor.saleOrderId == kernel_executor.resp_json.data.olpOrderDomain.saleSysOrderId
        # print "=============================="
        # print kernel_executor.integralOrderDomain
        # print "=============================="
        # print kernel_executor.blcOrderDomain
        # print "=============================="
        # print kernel_executor.olpOrderDomain
        # print "=============================="
        # print kernel_executor.payOrderId


if __name__ == "__main__":
    pass

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
