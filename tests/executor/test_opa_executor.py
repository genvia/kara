# -*- coding: utf-8 -*-

from pprint import pprint as pp

import kara
from kara.executor import *
from kara.database.util import *
from kara.validator import *


class TestOpaStdExecutor(object):
    def test_opa_std_executor_using_file(self):
        opa_executor = OpaStdHTTPExecutor("onlineorder.do", "opa_std_hf.py")
        # opa_executor = OpaStdHTTPExecutor("flowOrder.do", "opa_std_ll.py")
        # opa_executor = OpaStdHTTPExecutor("onlineorder.do", "opa_std_game.py")
        # opa_executor = OpaStdHTTPExecutor("sinopec/onlineorder.do", "opa_std_gascard.py")
        result = opa_executor.invoke()
        pp(opa_executor.raw)
        assert result.status_code == 200
        assert 'retcode>1</retcode>' in result.text
        assert '<err_msg></err_msg>' in result.text

        from lxml import etree as tree
        root = tree.fromstring(result.content)
        pp(root.xpath('//sporder_id')[0].text)
        pp(root.xpath('//game_userid')[0].text)
        pp(root.xpath('//game_state')[0].text)
        pp(root.xpath('//orderid')[0].text)
        pp(root.xpath('//cardname')[0].text)
        pp(root.xpath('//cardname')[0].text.encode('utf-8'))
        print root.xpath('//cardname')[0].text.encode('utf-8')
        assert root.xpath('//sporder_id')[0].text == opa_executor.raw[
            'payload']['sporder_id']
        sp = tree.Element("root", interesting='totally')
        pp(sp.get('orderid'))
        assert True

    def test_opa_std_executor_using_file_with_extra_params(self):
        import uuid
        sporder_id   = str(uuid.uuid1()) + '_000'
        opa_executor = OpaStdHTTPExecutor("onlineorder.do", "opa_std_hf.py", {"userid": "A10000009", "game_userid": "18909160000", "sporder_id": sporder_id})
        result = opa_executor.invoke()
        pp(opa_executor.raw)
        assert result.status_code == 200
        assert 'retcode>1</retcode>' in result.text
        assert '<err_msg></err_msg>' in result.text

        from lxml import etree as tree
        root = tree.fromstring(result.content)
        pp(root.xpath('//sporder_id')[0].text)
        pp(root.xpath('//game_userid')[0].text)
        pp(root.xpath('//game_state')[0].text)
        pp(root.xpath('//orderid')[0].text)
        pp(root.xpath('//cardname')[0].text)
        pp(root.xpath('//cardname')[0].text.encode('utf-8'))
        print root.xpath('//cardname')[0].text.encode('utf-8')
        assert root.xpath('//sporder_id')[0].text == opa_executor.raw[
            'payload']['sporder_id']
        sp = tree.Element("root", interesting='totally')
        pp(sp.get('orderid'))
        assert True


    def test_opa_std_executor_using_dict(self):
        params = {'cardid': '140000',
                  'md5_key': 'OFCARD',
                  'cardnum': '1',
                  'game_userid': '15243007235',
                  'sporder_time': '20161018130231',
                  'userid': 'A923506',
                  'userpws': 'OFCARD',
                  'version': '9.0'}
        import uuid
        params['sporder_id'] = str(uuid.uuid1())
        import hashlib
        md5obj = hashlib.md5()
        md5obj.update(params['userid'] + params['userpws'] + params[
            'cardid'] + params['cardnum'] + params['sporder_id'] + params[
                'sporder_time'] + params['game_userid'] + params['md5_key'])
        params['md5_str'] = md5obj.hexdigest().upper()

        opa_executor = OpaStdHTTPExecutor("onlineorder.do", params, False)
        result = opa_executor.invoke()
        pp(opa_executor.raw)
        assert result.status_code == 200

        if opa_executor.stricted:
            from lxml import etree as tree
            root = tree.fromstring(result.content)
            pp(root.xpath('//sporder_id')[0].text)
            pp(root.xpath('//game_userid')[0].text)
            pp(root.xpath('//game_state')[0].text)
            pp(root.xpath('//orderid')[0].text)
            pp(root.xpath('//cardname')[0].text)
            pp(root.xpath('//cardname')[0].text.encode('utf-8'))
            print root.xpath('//cardname')[0].text.encode('utf-8')
            assert root.xpath('//sporder_id')[0].text == opa_executor.raw[ 'payload']['sporder_id']
            sp = tree.Element("root", interesting='totally')
            pp(sp.get('orderid'))
        assert True

    def test_opa_std_simple_executor_has_sign(self):
        params = {'newKey': 'OFCARD', 'userid': 'A923506', 'userpws': 'OFCARD', 'version': '9.0'}

        opa_executor = OpaStdSimpleHTTPExecutor("modifyuserkey.do", params, ['userid', 'userpws', 'newKey'])
        result = opa_executor.invoke()
        pp(opa_executor.raw)
        assert result.status_code == 200
        assert 'retcode>1</retcode>' in result.text
        assert '<err_msg></err_msg>' in result.text

        from lxml import etree as tree
        root = tree.fromstring(result.content)
        pp(root.xpath('//userid')[0].text)
        assert root.xpath('//userid')[0].text == 'A923506'

    def test_opa_std_simple_executor_no_sign(self):
        params = {'pervalue': '1', 'phoneno': '13234341234',
                  'userid': 'A923506', 'userpws': 'OFCARD', 'version': '9.0'}

        opa_executor = OpaStdSimpleHTTPExecutor("telquery.do", params)
        result = opa_executor.invoke()
        pp(opa_executor.raw)
        assert result.status_code == 200

if __name__ == "__main__":
    pass

# vim: set ft=python ai rnu et ts=4 sw=4 tw=120:
