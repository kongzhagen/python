#!/usr/bin/env python
# _*_ coding:utf-8 _*_

def deco(arg):
    def __deco(func):
        def _deco(*args):
            print "before %s called ."%func.__name__
            return func(*args)
            print "end %s called ."%func.__name__
        return _deco
    return __deco

@deco('caca')
def myfunc(a,b):
    print "myfunc(%s,%s) called."%(a,b)
    return a + b

@deco('zaza')
def myfunc2(a,b,c):
    print "myfunc(%s,%s,%s) called."%(a,b,c)
    return a + b + c

print myfunc(1,2)
print myfunc2(1,2,3)

