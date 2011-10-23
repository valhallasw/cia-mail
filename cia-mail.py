#!/usr/bin/env python
#
# Copyright (C) Merlijn van Deen <valhallasw@gmail.com>, 2009-2011
# Distributed under the terms of the MIT license.
#
import sys
from optparse import OptionParser

get_class_by_name = lambda name: reduce(getattr, name.split('.')[1:], __import__(name.split('.')[0]))

parser = OptionParser(usage = "usage: %prog [options] <cia project name>  < email")
parser.add_option("-v", "--verbose",
                  action="store_true",
                  default = False,
                  help = "Show XMLRPC request and response")
parser.add_option("-c", "--class",
                  dest="classname",
                  default="cia.GenericMailToCIA",
                  help = "Define class to use as mail parser")
(options, args) = parser.parse_args()
if len(args) != 1:
    parser.print_help()
    sys.exit()

RunClass = get_class_by_name(options.classname)
parms  = (sys.stdin, args[0], options.verbose)
if options.verbose:
    print "Running %s%r.commit()" % (RunClass, parms)

RunClass(*parms).commit()
