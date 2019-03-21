# -*- coding: utf-8 -*-

from lxml import etree as tree

from kara.common              import karaerror
from kara.validator.validator import Validator
from kara.validator.validator import register_validator


@register_validator
class XPathValidator(Validator):
    prefix     = '/'
    prefix_len = len(prefix)

    def is_supported(self, obj, cond, target):
        return cond and len(cond) > self.prefix_len and cond[0:self.prefix_len] == self.prefix and isinstance(obj, basestring) and obj and isinstance(target, basestring) and target and True

    def _verify_internal(self,  obj, cond, target):
        is_ok = False

        try:
            root = tree.fromstring(obj)
            if len(root.xpath(cond)) == 1 and root.xpath(cond)[0].text == target:
                is_ok = True
        except Exception, e:
            # TODO: lose exception!
            pass
            print e

        return is_ok

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
