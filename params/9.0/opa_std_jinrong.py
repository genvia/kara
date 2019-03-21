# -*- coding: utf-8 -*-

import time
import uuid
import random
import hashlib

import kara

userid            = random.choice(kara.conf.params.opa.mids)
bankId            = '102100099996'
cardId            = '6101800'
bankCardNo        = '1111111'
payeeName         = 'jjj'
transferMoney     = '100'
remitterPhone     = '1340000' + str(random.randint(1, 9999)).zfill(4)
sporderId         = str(uuid.uuid1())


userpws = kara.conf.params.opa.userpwd
retUrl  = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
KeyStr = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid + userpws + cardId + bankId + bankCardNo + payeeName + transferMoney + sporderId + KeyStr)
md5Str  = md5obj.hexdigest().upper()

# fake parameters, because game_userid and sporder_id been validated in executor!
game_userid = bankCardNo
sporder_id = sporderId

del time
del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
