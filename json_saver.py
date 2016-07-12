#!/usr/bin/env python

import json
from sys import argv

def json_in(filename):
    fh = open(filename)
    contents = json.load(fh)
    print "Here's your file %r:" % filename
    print contents

def to_csv():
    pass

def main():
    script, filename = argv
    json_in(filename)
	

if __name__ == '__main__':
    main()
