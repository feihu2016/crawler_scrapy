# -*- coding: utf-8 -*-
#from scrapy import log
import logging as log

def warn(msg):
    log.warn(msg)


def info(msg):
    log.info(msg)


def debug(msg):
    log.debug(msg)

import pprint
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
pu = MyPrettyPrinter()

pp = pprint.PrettyPrinter()

