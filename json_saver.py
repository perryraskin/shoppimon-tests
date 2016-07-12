#!/usr/bin/env python

import json
import sys

def json_in(fh):
    contents = json.load(fh)
    print "Here's your file:"
    print contents

def to_csv():
    pass

def main():
    json_in(sys.stdin)
	

if __name__ == '__main__':
    main()
