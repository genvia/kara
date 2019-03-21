# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

import kara
from kara.common import karaerror


class AbstractHTTPExecutor(object):
    def logging(self, msg, level=0):
        kara.logger.info("{}: {}", self.__class__.__name__, msg)

    def __construct_url(self):
        return "http://" + self.host + ":" + self.port + "/" + self.path

    url = property(__construct_url)

    def _get(self, *args, **kwargs):
        raise NotImplementedError()

    def _post(self, *args, **kwargs):
        raise NotImplementedError()

    def _login(self, *args, **kwargs):
        raise NotImplementedError()

    def invoke(self, *args, **kwargs):
        if self.method == 'POST':
            return self._post(*args, **kwargs)
        elif self.method == 'GET':
            return self._get(*args, **kwargs)
        elif self.method == 'LOGIN':
            return self._login(*args, **kwargs)
        else:
            raise karaerror.KaraExecutorError("http method do not support.")

    def __getattr__(self, attrname):
        return self.raw.get(attrname)

    def __build_params(self):
        # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT

        if isinstance(self.parameters, basestring) and self.parameters.endswith(".py"):
            try:
                opa_ver_path = kara.conf.params.opa.version if self.parameters.startswith('opa_') else ''
                ret_locals = self.extra_params.copy()
                execfile(join(kara.KARA_HOME, kara.PARAM_FILE_DIR, opa_ver_path, self.parameters), globals(), ret_locals)
            except Exception, e:
                raise karaerror.KaraExecutorError(e.message)

            # OLD code:
            # payload = vars().copy()
            # del payload['self']
            # NEW code:
            # for with extra parameters!
            payload = ret_locals.copy()
            # import sys; import pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()  # XXX BREAKPOINT
        elif isinstance(self.parameters, dict):
            payload = self.parameters
        else:
            raise karaerror.KaraExecutorError(
                "parameters is't a dict or a validate python file.")

        return payload


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
