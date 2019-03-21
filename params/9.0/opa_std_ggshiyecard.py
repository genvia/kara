# -*- coding: utf-8 -*-

import uuid
import random
import hashlib

import kara

userid            = random.choice(kara.conf.params.opa.mids)
provId            = kara.conf.params.opa.ggshiye_provId
cardId            = '640103'
cardnum           = '1'
account           = '1'
sporderId         = str(uuid.uuid1())


userpws = kara.conf.params.opa.userpwd
retUrl  = kara.conf.params.opa.callback_url
version = kara.conf.params.opa.version
KeyStr = kara.conf.params.opa.md5_key

md5obj  = hashlib.md5()
md5obj.update(userid+userpws+provId+cardId+cardnum+account+sporderId+KeyStr)
md5_str  = md5obj.hexdigest().upper()

# fake parameters, because game_userid and sporder_id been validated in executor!
game_userid = account
sporder_id = sporderId

del uuid
del random
del hashlib

del kara
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

