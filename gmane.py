# Copyright (C) Merlijn van Deen <valhallasw@gmail.com>, 2011
# Distributed under the terms of the MIT license.

import cia
import httplib
import urllib

class MLwithGmaneUrlToCIA(cia.RemoveMLNameToCIA):
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
      <url>%(url)s</url>
      <threadid>%(threadid)s</threadid>
      <msgid>%(msgid)s</msgid>
    </commit>
  </body>
</message>""" 
    def initialize(self):
        cia.RemoveMLNameToCIA.initialize(self)
        c = httplib.HTTPConnection("news.gmane.org")
        c.request("HEAD", "/find-root.php?" + urllib.urlencode(
            {'message_id': self.headers['Message-ID']}))
        r = c.getresponse()
        self.url = r.getheader('location')
        self.threadid = self.url.split('/')[4]
        try:
            self.msgid    = self.url.split('/')[5].split('=')[-1]
        except IndexError:
            self.msgid    = ''
