# -*- coding: utf-8 -*-


class KaraBaseError(Exception):
    pass


class KaraExecutorError(KaraBaseError):
    pass


class KaraDatabaseError(KaraBaseError):
    pass


class KaraValidatorError(KaraBaseError):
    pass


if __name__ == "__main__":
    pass

# vim: set ft=python ai nu et ts=4 sw=4 tw=120:
