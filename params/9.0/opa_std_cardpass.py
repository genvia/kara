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

    userid       = random.choice(kara.conf.params.opa.mids)
    phone        = random.choice(kara.conf.params.opa.hf_prefix) + str(random.randint(1, 9999)).zfill(4)
    email        = "Oftester@163.com"
    sporder_id   = str(uuid.uuid1())
    sporder_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    # 京东E卡5元卡密
    cardid       = '1227400'
    cardnum      = '1'

    userpws = kara.conf.params.opa.userpwd
    ret_url = kara.conf.params.opa.callback_url
    version = kara.conf.params.opa.version
    md5_key = kara.conf.params.opa.md5_key

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
md5obj.update(userid + userpws + cardid + cardnum + sporder_id + sporder_time + md5_key)
md5_str = md5obj.hexdigest().upper()
################################################################################

del hashlib
del md5obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

