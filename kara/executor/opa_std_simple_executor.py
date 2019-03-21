# -*- coding: utf-8 -*-

import requests
from lxml import etree as tree
import hashlib

import kara
from kara.common import karaerror
from kara.executor import abstract_executor


class OpaStdSimpleHTTPExecutor(abstract_executor.AbstractHTTPExecutor):
    def __init__(self, path, parameters_data, sign_keys=None, sign_name='md5_str', post_code='OFCARD', stricted=True, method='POST'):
        self.host       = kara.conf.uts.opa.host
        self.port       = kara.conf.uts.opa.port
        self.path       = path
        self.method     = method
        self.parameters = parameters_data
        # TODO: not used?
        self.stricted   = stricted
        self.sign_keys  = None if sign_keys is None else sign_keys
        self.sign_name  = sign_name
        self.post_code  = post_code

    def _post(self, *args, **kwargs):
        payload = self._AbstractHTTPExecutor__build_params()

        if self.sign_keys:
            sign_list = [self.parameters.get(key, '') for key in self.sign_keys]
            sign_str  = ''.join(sign_list).decode("utf-8").encode("GBK") + self.post_code
            md5_obj   = hashlib.md5()
            md5_obj.update(sign_str)
            payload[self.sign_name] = md5_obj.hexdigest().upper()

        last_querystring = '&'.join(['='.join( [k, v]) for k, v in payload.items() if isinstance(v, str)])

        self.raw = dict()
        self.raw['querystring'] = self.url + '?' + last_querystring
        self.raw['payload'] = payload

        # TODO: don't use eval, has other better style?
        method = eval("requests." + self.method.lower())
        self.raw['response'] = method(self.url, params=payload)

        self.raw['resp_text'] = self.raw['response'].text.encode("utf-8").replace("GB2312", "utf8").replace("gb2312", "utf8")

        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        if self.raw['response'].status_code != 200:
            raise karaerror.KaraExecutorError("opaStd http executor invoke failure! status code is't 200.")

        return self.raw['response']


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
