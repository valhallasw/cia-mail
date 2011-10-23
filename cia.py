# Copyright (C) Merlijn van Deen <valhallasw@gmail.com>, 2009-2011
# Distributed under the terms of the MIT license.

import sys, time
from email.Parser import Parser
from email.Header import Header, decode_header
from xml.sax.saxutils import escape
from xmlrpclib import ServerProxy

verbose = ("-v" in sys.argv)

class GenericMailToCIA(object):
    _CIAmessage = """<message>
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
</message>""" 

    def __init__(self, message, project, verbose=False):
        self._parse_message(message)
        self.initialize()
        self.project = project
        self.verbose = verbose

    def initialize(self):
        pass

    def _parse_message(self, message):
        e = Parser().parse(message)

        # Stupid email library. This parses all headers into nice unicode strings...
        self.headers = dict([(header, ' '.join([text.decode(encoding or 'ascii') for (text, encoding) in decode_header(e[header])])) for header in e.keys()])

    @property
    def author(self):
        author = self.headers['From']
        author = author[:author.find('<')].strip() # remove email address
        author = author.strip("\"\'")
        return author

    @property
    def subject(self):
        subject = self.headers['Subject']
        subject = subject.replace('\n', ' ')
        return subject
    
    @property
    def timestamp(self):
        return int(time.time())

    @property
    def CIAmessage(self):
        return self._CIAmessage % self

    def commit(self):
        if self.verbose:
            print self.CIAmessage
        result = ServerProxy('http://cia.vc/RPC2').hub.deliver(self.CIAmessage)
        if verbose:
            print result

    def __getitem__(self, attr):
        data = getattr(self, attr)
        if isinstance(data, basestring):
            data = escape(data)
        return data

class RemoveMLNameToCIA(GenericMailToCIA):
    @property
    def subject(self):
       import re
       return re.sub(r'\[.+?\]', '', GenericMailToCIA.subject.fget(self)).strip()

