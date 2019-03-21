# -*- coding: utf-8 -*-

import sys
import requests
from lxml import etree as tree

import kara
from kara.common import karaerror
from kara.executor import abstract_executor


class OpaStdHTTPExecutor(abstract_executor.AbstractHTTPExecutor):
    def __init__(self, path, parameters_data, fetch_billid=False, extra_params=None, method='POST'):
        self.host         = kara.conf.uts.opa.host
        self.port         = kara.conf.uts.opa.port
        self.path         = path
        self.method       = method
        self.parameters   = parameters_data
        self.extra_params = extra_params if extra_params else {}
        self.fetch_billid = fetch_billid

    def _post(self, *args, **kwargs):
        # import pudb; pudb.set_trace()  # XXX BREAKPOIN
        payload = self._AbstractHTTPExecutor__build_params()
        last_querystring = '&'.join(['='.join(
            [k, v]) for k, v in payload.items() if isinstance(v, str)])

        self.raw = dict()
        self.raw['querystring'] = self.url + '?' + last_querystring
        self.raw['payload'] = payload

        # TODO: don't use eval, has other better style?
        method = eval("requests." + self.method.lower())
        self.raw['response'] = method(self.url, params=payload)

        # lxml has encoding declare!
        self.raw['resp_text'] = self.raw['response'].text.encode("utf-8").replace("GB2312", "utf8").replace("gb2312", "utf8")

        # import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        if self.raw['response'].status_code != 200:
            raise karaerror.KaraExecutorError("opaStd http executor invoke failure! status code is't 200.")

        if self.fetch_billid:
            if "<retcode>1</retcode>" not in self.raw['resp_text'] or "<err_msg></err_msg>" not in self.raw['resp_text']:
                raise karaerror.KaraExecutorError("opaStd http executor invoke result roughly validate in executor failure.")
            root = tree.fromstring(self.raw['response'].content)
            self.raw['billid'] = root.xpath("//orderid")[0].text

        self.raw['oflinkid'] = self.raw['payload']['sporder_id']
        self.raw['userid']   = self.raw['payload']['userid']
        if 'game_userid' in self.raw['payload']:
            self.raw['game_userid'] = self.raw['payload']['game_userid']

        return self.raw['response']


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
