import logging

logging.basicConfig(level=logging.DEBUG)


import ssl
import sys
import logging
import getpass
import socket
from sleekxmpp import Iq, ClientXMPP
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
from sleekxmpp.exceptions import IqError, IqTimeout

import iq3 #custom stuff for iQ3 unit

import sleekxmpp
from flask import Flask, request, render_template # API Stuff

from config import config

class scorpio(sleekxmpp.ClientXMPP):

    """
    Class for setting up the scorpio login and shit
    this then defines all the functions which go to get spaWned for the mother fucking API
    """

    def __init__(self, jid, password, to, resource):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.to = to
        self.Resource = resource

    def setchan(self,channel):

        try:
            out = self['iq3'].set_viewing(self.jid, self.to, self.Resource, channel)
            try:
                error = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}error').text
                if(error=="failed"):
                    return "Change failed"
            except:
                return "Error?"
            try:
                response = out.xml.find('{foxtel:iq}current_viewing/{foxtel:iq}response').text
                if(response=="OK"):
                    return "Channel changed to " + str(channel)
            except:
                return "Some other error???"

        except IqError as e:
            return "Error " + str(e)
        except IqTimeout:
            return "The bitch aint responding"






app = Flask(__name__)

xmpp = scorpio(config.loginjid, config.loginpw, config.tojid, config.resource)
xmpp.register_plugin('xep_0030') # Service Discovery
xmpp.register_plugin('xep_0004') # Data Forms
xmpp.register_plugin('xep_0060') # PubSub
xmpp.register_plugin('xep_0199') # XMPP Ping
xmpp.register_plugin('iq3', module=iq3)

@app.route('/roster')
def index():
    resp = scorpio.setchan(channel='123')
    return resp

def session_start(e):
    xmpp.get_roster()
    xmpp.send_presence()

xmpp.add_event_handler('session_start', session_start)

if __name__ == '__main__':
    xmpp.connect()
    xmpp.process()
    app.run(port=5000)
