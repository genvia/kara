# -*- coding: utf-8 -*-
# only for setup.py's findpackages

from jsonpath_rw import parse, jsonpath

from kara.common              import karaerror
from kara.validator.validator import Validator
from kara.validator.validator import register_validator


@register_validator
class JsonPathValidator(Validator):
    prefix     = '$'
    prefix_len = len(prefix)

    def is_supported(self, obj, cond, target):
        return cond and len(cond) > self.prefix_len and cond[0:self.prefix_len] == self.prefix and isinstance(obj, dict) and obj and isinstance(target, basestring) and target and True

    def _verify_internal(self,  obj, cond, target):
        is_ok = False

        try:
            json_expr  = parse(cond)
            node_value = json_expr.find(obj)[0].value
            if node_value == target:
                is_ok = True
        except Exception, e:
            # TODO: lose exception!
            pass
            print e

        return is_ok

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:

