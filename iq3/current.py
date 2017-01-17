import logging

from sleekxmpp.stanza import StreamFeatures, Iq
from sleekxmpp.xmlstream import register_stanza_plugin, JID
from sleekxmpp.plugins import BasePlugin
from iq3 import stanza, current_programme, diagnostic_tuner, current_viewing
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher.id import MatcherId
import xml.etree.ElementTree as ET


class iq3(BasePlugin):

    name = 'iq3'
    description = 'my iq3'


    def plugin_init(self):
        register_stanza_plugin(Iq, current_programme)
        register_stanza_plugin(Iq, diagnostic_tuner)
        register_stanza_plugin(Iq, current_viewing)

        self.sessions = {};

    def get_current(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        iq.enable('current_programme')
        resp = iq.send(block=True);

        return resp

    def get_diag(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'get'
        iq.enable('diagnostic_tuner')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "diagnostic_tuner", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp

    def set_viewing(self, jid=None, tjid=None, resource=None):
        seqnr = "12345"
        iq = self.xmpp.Iq()
        iq['from'] = jid + "/" + resource
        iq['to'] = tjid + "/" + resource
        iq['id'] = seqnr
        iq['xml:lang'] = 'en'
        iq['type'] = 'set'
        iq.enable('current_viewing')
        self.sessions[seqnr] = {"from": iq['from'], "to": iq['to'], "seqnr": seqnr, "name": "current_viewing", "namespace": "foxtel:iq"};
        resp = iq.send(block=True)

        return resp
