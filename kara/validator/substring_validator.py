# -*- coding: utf-8 -*-

from kara.common              import karaerror
from kara.validator.validator import Validator
from kara.validator.validator import register_validator


@register_validator
class SubStringValidator(Validator):
    prefix = '~'
    prefix_len = len(prefix)

    def is_supported(self, obj, cond, target):
        return cond and len(cond) > self.prefix_len and cond[
            0:self.prefix_len] == self.prefix and isinstance(
                obj, basestring) and obj and isinstance(target, basestring) and target and True

    def _verify_internal(self, obj, cond, target):
        return target in obj

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
