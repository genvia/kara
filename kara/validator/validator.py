# -*- coding: utf-8 -*-

import abc

from kara.common import karaerror

class Validator(object):
    __metaclass__ = abc.ABCMeta

    members= {}

    @abc.abstractmethod
    def is_supported(self, obj, condition):
        pass

    def verify(self, obj, condition, target):
        if not self.is_supported(obj, condition, target):
            raise karaerror.KaraValidatorError("condition is invalid.")
        return self._verify_internal(obj, condition, target)

    @abc.abstractmethod
    def _verify_internal(self, obj, condition):
        pass

    @staticmethod
    def batch_verify(obj, *conditions):
        if not conditions or (len(conditions) % 2):
            raise karaerror.KaraValidatorError("condition ammount are invalid.")

        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        for cond_pair in [(conditions[2*i], conditions[2*i+1]) for i in xrange(len(conditions) / 2)]:
            key = cond_pair[0][:1]
            validator = Validator.members[key]
            if not validator.verify(obj, cond_pair[0], cond_pair[1]):
                return False

        return True

def register_validator(clz):
    if clz not in Validator.members:
        Validator.members[clz.prefix] = clz()
    return clz

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
