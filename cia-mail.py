#!/usr/bin/env python
#
# Copyright (C) Merlijn van Deen <valhallasw@gmail.com>, 2009
#
# Distributed under the terms of the MIT license.
#

import sys, time
from email.Parser import Parser
from email.Header import Header, decode_header
from xml.sax.saxutils import escape
from xmlrpclib import ServerProxy

verbose = ("-v" in sys.argv)

e = Parser().parse(sys.stdin)

# Stupid email library. This parses all headers into nice unicode strings...
headers = dict([(header, ' '.join([text.decode(encoding or 'ascii') for (text, encoding) in decode_header(e[header])])) for header in e.keys()])

author = headers['From']
author = author[:author.find('<')].strip() # remove email address
author = author.strip("\"\'")

subject = headers['Subject']
subject = subject.replace('\n', ' ')

message = """
<message>
  <generator>
    <name>CIA Python client for mail</name>
    <version>0.2</version>
  </generator>
  <source>
    <project>%(project)s</project>
  </source>
  <timestamp>%(timestamp)s</timestamp>
  <body>
    <commit>
      <author>%(author)s</author>
      <log>%(subject)s</log>
    </commit>
  </body>
</message>""" % {
    'project'  : escape(sys.argv[1]),
    'timestamp': int(time.time()),
    'author'   : escape(author.encode('utf-8')),
    'subject'  : escape(subject.encode('utf-8'))
    }

if verbose:
   print message

result = ServerProxy('http://cia.vc/RPC2').hub.deliver(message)
if verbose:
   print result
