# -*- coding: utf-8 -*-

import json
import collections
import requests

from kara.common import karaerror
from kara.executor import abstract_executor

class OfrgFetchOrderHTTPExecutor(abstract_executor.AbstractHTTPExecutor):
    FetchObject = collections.namedtuple("fetchObj", "billid supuid")

    def __init__(self, host, path="getOrderNew", port='8080', method='POST'):
        self.host = host
        self.path = path
        self.port = port
        self.method = method

    def _post(self, parameters):
        if isinstance(parameters, dict):
            payload = parameters
        else:
            raise karaerror.KaraExecutorError(
                "ofrg fetch executor only apply a dict type parameters.")
        from pprint import pprint as pp
        pp(payload)

        last_querystring = '&'.join(['='.join([k, str(v)]) for k, v in payload.items()])
        self.raw = dict()
        self.raw['querystring'] = self.url + '?' + last_querystring
        self.raw['payload'] = payload

        # TODO: don't use eval, has other better style?
        method = eval("requests." + self.method.lower())
        self.raw['response'] = result = method(self.url, params=payload)
        result_string = result.text.encode('utf-8')

        json_obj = json.loads(result_string)
        if not json_obj['success'] or json_obj['code'] != '1':
            raise karaerror.KaraExecutorError("ofrg fetch order failure.")

        self.raw['count'] = json_obj['totalCount']
        self.raw['real_success'] = True if json_obj['totalCount'] > 0 else False
        for data in json_obj['data']:
            self.raw[data['orderId']] = self.FetchObject(billid=data['orderId'], supuid=data['supUid'])

        return self.raw['response']


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
