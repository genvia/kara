# -*- coding: utf-8 -*-

import time
import uuid
import random
import hashlib

import kara

index        = random.randint(0, len(kara.conf.params.opa.game_card_id)-1)

userid       = random.choice(kara.conf.params.opa.mids)
game_userid  = "kara@ofpay.com"
game_userpsw = "kara"
sporder_id   = str(uuid.uuid1())
sporder_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
cardid       = kara.conf.params.opa.game_card_id[index]
game_area    = kara.conf.params.opa.game_game_area[index]
game_srv     = kara.conf.params.opa.game_game_srv[index]
cardnum      = '1'
phoneno      = "13913913913"

userpws = kara.conf.params.opa.userpwd
ret_url = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
md5_key = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid + userpws + cardid + cardnum + sporder_id + sporder_time + game_userid + game_area + game_srv + md5_key)
md5_str = md5obj.hexdigest().upper()

del index

del time
del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:



