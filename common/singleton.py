#!/usr/bin/env python
# encoding: utf-8

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class TestSingleton(Singleton):
    value = 1


if __name__ == "__main__":
    t1 = TestSingleton()
    t2 = TestSingleton()

    print id(t1)
    print id(t2)
