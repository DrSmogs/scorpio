import logging

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin
from iq3 import stanza, Current, diagnostic_tuner, current_viewing
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher.id import MatcherId
import xml.etree.ElementTree as ET


class iq3(BasePlugin):

 name = 'iq3'
 description = 'my iq3'
 #dependencies = set(['iq3'])
 stanza = stanza

 def plugin_init(self):
  register_stanza_plugin(Iq, Current)
  register_stanza_plugin(Iq, diagnostic_tuner)
  register_stanza_plugin(Iq, current_viewing)
  #self.xmpp.register_handler(
   #Callback('Current_programme',
   #StanzaPath('iq@type=result/current_programme'),
   #self._handle_event_cur))
  

  self.sessions = {};

 def get_current(self, jid=None, tjid=None, resource=None):
    seqnr = "12345"
    iq = self.xmpp.Iq()
    iq['from'] = jid + "/" + resource
    iq['to'] = tjid + "/" + resource
    iq['id'] = seqnr
    iq['type'] = 'get'
    iq['xml:lang'] = 'en'
    iq.enable('current_programme')
    #iq.enable('current')a
    #self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "callback": callback , "name": "current_programme", "namespace": "foxtel:iq"};
    #self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_programme", "namespace": "foxtel:iq"};
    seqnr = iq.send(block=True);

    return seqnr

 def get_diag(self, jid=None, tjid=None, resource=None):
    seqnr = "123456"
    iq = self.xmpp.Iq()
    iq['from'] = jid + "/" + resource
    iq['to'] = tjid + "/" + resource
    iq['id'] = seqnr
    iq['type'] = 'get'
    iq['xml:lang'] = 'en'
    iq.enable('diagnostic_tuner')
    self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "diagnostic_tuner", "namespace": "foxtel:iq"};
    seqnr = iq.send(block=True)

    return seqnr

 def set_viewing(self, jid=None, tjid=None, resource=None):
    seqnr = "1234567"
    iq = self.xmpp.Iq()
    iq['from'] = jid + "/" + resource
    iq['to'] = tjid + "/" + resource
    iq['id'] = seqnr
    iq['type'] = 'set'
    iq['xml:lang'] = 'en'
    iq['current_viewing']['current_channel'] = '123'
    iq.enable('current_viewing')
    self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
    seqnr = iq.send(block=True)

    return seqnr

 def _handle_event_cur(self, iq):
   print("handle trig")
   mystring = str(iq['current_programme'])
   print("--- ")
   #print(iq.keys())
   print(iq['current_programme']['p'])
   print(iq['current_programme'].keys())
   print("  ")
   root = ET.fromstring(mystring)
   length = root[0][0].text
   name = root[0][1].text
   genre = root[0][2].text
   parRating = root[0][3].text
   start_time = root[0][4].text
   synopsys = root[0][5].text
   print("Boxy is watching ", name)


    

    


