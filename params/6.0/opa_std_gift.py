# -*- coding: utf-8 -*-

import time
import uuid
import random
import hashlib

import kara

userid            = random.choice(kara.conf.params.opa.mids)
cardid            = '148063'
cardnum           = '1'
game_userid     = '1340000' + str(random.randint(1, 9999)).zfill(4)
sporder_id         = str(uuid.uuid1())


userpws = kara.conf.params.opa.userpwd
retUrl  = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
KeyStr = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid + userpws + cardid + cardnum + game_userid + sporder_id + KeyStr)
md5Str  = md5obj.hexdigest().upper()

# fake parameters, because game_userid and sporder_id been validated in executor!


del time
del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
