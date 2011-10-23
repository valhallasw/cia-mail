#!/usr/bin/env python
#
# Copyright (C) Merlijn van Deen <valhallasw@gmail.com>, 2009
#
# Distributed under the terms of the MIT license.
#

import cia

class SFBugMailToCIA(cia.RemoveMLNameToCIA):
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
      <itemid>%(itemid)s</itemid>
    </commit>
  </body>
</message>""" 

    @property
    def author(self):
        author = self.headers['X-SourceForge-Tracker-itemupdate-username']
        return author

    @property
    def subject(self):
        subject = cia.RemoveMLNameToCIA.subject.fget(self)
        subject += " (%s)" % (self.headers['X-SourceForge-Tracker-itemupdate-reason'],)
        return subject
    
    @property
    def itemid(self):
        return self.headers['X-SourceForge-Tracker-itemid']
