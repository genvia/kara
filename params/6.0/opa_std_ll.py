# -*- coding: utf-8 -*-

import time
import uuid
import random
import hashlib

import kara

index           = random.randint(0, len(kara.conf.params.opa.ll_phone_prefix)-1)

userid          = random.choice(kara.conf.params.opa.mids)
phoneno         = kara.conf.params.opa.ll_phone_prefix[index] + str(random.randint(1, 9999)).zfill(4)
flowValue       = kara.conf.params.opa.ll_flow_value[index]
sporderId       = str(uuid.uuid1())
perValue        = '3'
range           = '2'
effectStartTime = '1'
effectTime      = '1'
netType         = '4G'


userpws = kara.conf.params.opa.userpwd
retUrl  = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
md5_key = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid + userpws + phoneno + perValue + flowValue + range + effectStartTime + effectTime + netType + sporderId + md5_key)
md5Str  = md5obj.hexdigest().upper()

# fake parameters, because game_userid and sporder_id been validated in executor!
game_userid = phoneno
sporder_id  = sporderId

del index

del time
del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

