# -*- coding: utf-8 -*-

import time
import uuid
import random
import hashlib

# TODO: why not run in pytest where used relatived impport
# from . import common_params
# from kara.executor.params import common_params
import kara

userid       = random.choice(kara.conf.params.opa.mids)
cardnum      = '30'
teltype      = '1'
chargeType   = '1'
game_userid  = '025-' + time.strftime("%d%H%M%S", time.localtime())
sporder_id   = str(uuid.uuid1())
sporder_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

userpws = kara.conf.params.opa.userpwd
ret_url = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
KeyStr = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid + userpws + cardnum + sporder_id + sporder_time + game_userid + KeyStr)
md5_str = md5obj.hexdigest().upper()

del time
del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
