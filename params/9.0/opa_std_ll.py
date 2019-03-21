# -*- coding: utf-8 -*-

old_extra_params = locals().copy()

def func_set_orignal_values():
    ################################################################################
    # 一般尽量只修改下面的部分来设置参数，文件的其它部分不清楚不要动
    ################################################################################

    import time
    import uuid
    import random
    # TODO: why not run in pytest where used relatived impport
    # from . import common_params
    # from kara.executor.params import common_params
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


    del index

    del time
    del uuid
    del random
    del kara

    ################################################################################
    # 一般尽量只修改上面的部分来设置参数，文件的其它部分不清楚不要动
    ################################################################################

    return vars()

locals().update(func_set_orignal_values())
locals().update(old_extra_params)
del old_extra_params
del func_set_orignal_values

import hashlib
md5obj  = hashlib.md5()
################################################################################
# 这句拼参数，不同接口可能是不一样的，有可能需要修改，同样其它地方不清楚不要动
md5obj.update(userid + userpws + phoneno + perValue + flowValue + range + effectStartTime + effectTime + netType + sporderId + md5_key)
# 有时验签的key也不一致，流量是md5Str
md5Str = md5obj.hexdigest().upper()
################################################################################

# fake parameters, because game_userid and sporder_id been validated in executor!
game_userid = phoneno
sporder_id  = sporderId


del hashlib
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
