import sys
import os
import subprocess
import argparse
import datetime


tracelevel = 4

def trace(level, *args):
    def mywrite(thing):
        sys.stdout.write(mystr(thing))
    def mystr(thing):
        try:
            return str(thing)
        except UnicodeEncodeError:
            return unicode(thing).encode('ascii', 'ignore')

    if tracelevel >= level:
        mywrite( datetime.datetime.now().strftime("%H:%M:%S: ") )
        if isinstance(args[0], (list, tuple)):
            for s in args[0]:
                mywrite(s)
        else:
            for count, thing in enumerate(args):
                mywrite(thing)                
        print '' # newline

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))

def is_iterable(item):
    #add types here you don't want to mistake as iterables
    if isinstance(item, basestring): 
        return False

    #Fake an iteration.
    try:
        for x in item:
            return True;
    except TypeError:
        return False