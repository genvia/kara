# -*- coding: utf-8 -*-

import requests
import json
from argparse import Namespace

import kara
from kara.common import karaerror
from kara.executor import abstract_executor


class KernelNormalHTTPExecutor(abstract_executor.AbstractHTTPExecutor):
    def __init__(self, path, parameters_data, method='POST'):
        self.host         = kara.conf.uts.kernel.host
        self.port         = kara.conf.uts.kernel.port
        self.path         = path
        self.method       = method
        self.parameters   = parameters_data
        self.extra_params = {}


    def _data_from_file(self):
        return isinstance(self.parameters, basestring) and self.parameters.endswith(".py")

    def _post(self, *args, **kwargs):
        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        payload = self._AbstractHTTPExecutor__build_params()
        if not self._data_from_file():
            payload['template_str'] = json.dumps(payload)
            self.logging("data from dict.")

        self.logging("payload: " + payload['template_str'])
        try:
            self.raw = dict()
            self.raw['payload'] = json.loads(payload['template_str'], object_hook=lambda d: Namespace(**d))

            request_sub_obj = self.raw['payload'].payRequest
            for item in kara.conf.misc.kernel_payment_keys:
                if hasattr(request_sub_obj, item):
                    self.raw[item] = getattr(request_sub_obj, item)

            method_sub_obj = self.raw['payload'].payMethod
            for item in kara.conf.misc.kernel_method_keys:
                if hasattr(method_sub_obj, item):
                    self.raw[item] = getattr(method_sub_obj, item)
        except Exception, e:
            raise karaerror.KaraExecutorError("kernel normal http executor handle template data exception.")

        # TODO: don't use eval, has other better style?
        method = eval("requests." + self.method.lower())
        self.raw['response'] = method(self.url, json=json.loads(payload['template_str']))

        self.logging("response text \n" + self.raw['response'].text)
        if self.raw['response'].status_code != 200:
            raise karaerror.KaraExecutorError("kernel normal http executor invoke response failure.")

        try:
            self.raw['resp_json'] = json.loads(self.raw['response'].text, object_hook=lambda d: Namespace(**d))

            self.raw['code']                = self.raw['resp_json'].code
            self.raw['payOrderId']          = self.raw['resp_json'].data.payOrderId
            self.raw['olpOrderDomain']      = self.raw['resp_json'].data.olpOrderDomain
            self.raw['blcOrderDomain']      = self.raw['resp_json'].data.blcOrderDomain
            self.raw['integralOrderDomain'] = self.raw['resp_json'].data.integralOrderDomain
        except Exception, e:
            raise karaerror.KaraExecutorError("kernel normal http executor handle response exception.")

        return self.raw['response']


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
