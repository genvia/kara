# -*- coding: utf-8 -*-

import requests

from kara.common import karaerror
from kara.executor import abstract_executor


class OfrgCallbackHTTPExecutor(abstract_executor.AbstractHTTPExecutor):
    _default_payload = {'outorderid': 'NOT_USED',
                        'card_no': 'NOT_USED',
                        'remark': 'KARA_CALL_FOR_U',
                        'limittype': 1}

    def __init__(self, host, path, port='8080', method='POST'):
        self.host = host
        self.path = path
        self.port = port
        self.method = method

    def _post(self, parameters):
        payload = self._default_payload
        payload.update(parameters)

        last_querystring = '&'.join(['='.join([k, str(v)]) for k, v in payload.items()])
        self.raw = dict()
        self.raw['querystring'] = self.url + '?' + last_querystring
        self.raw['payload'] = payload

        # TODO: don't use eval, has other better style?
        method = eval("requests." + self.method.lower())
        self.raw['response'] = result = method(self.url, params=payload)
        result.string = result.text.encode('utf-8')

        if result.string != "success":
            raise karaerror.KaraExecutorError("ofrg callback failure.")

        self.raw['resp_text'] = result.string
        return self.raw['response']


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
