#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import ssl
import sys
import logging
import getpass
from optparse import OptionParser
from sleekxmpp import Iq
from sleekxmpp.xmlstream import ElementBase, register_stanza_plugin, ET
import socket
from sleekxmpp.exceptions import IqError, IqTimeout
import iq3

import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

#def setstop_any_script(self, stop_any_script):
# self.addfield('true')

#def addField(self, name):
# self.xml.append('test')



class EchoBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """

    def __init__(self, jid, password, to, resource):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.to = to
        self.Resource = resource

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        #self.add_event_handler("result", self._response)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        #self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """

        self.send_presence()
        self.get_roster()

        try:
          current = self['iq3'].get_current(self.jid, self.to, self.Resource)
          print(current.xml.find('{foxtel:iq}current_programme/{foxtel:iq}programme/{foxtel:iq}event_name').text)

        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")

        try:
         diag = self['iq3'].get_diag(self.jid, self.to, self.Resource)
         print()
         print(diag.xml.items())
        

        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")



        try:
         channel = self['iq3'].set_viewing(self.jid, self.to, self.Resource)
         print()
         print(channel.xml.items())

        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")

        try:
         info = self['iq3'].get_info(self.jid, self.to, self.Resource)
         print()
         print(info.xml.items())


        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")


        try:
         volume = self['iq3'].get_volume(self.jid, self.to, self.Resource)
         print()
         print(volume.xml.items())


        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")

        try:
         volume = self['iq3'].set_volume(self.jid, self.to, self.Resource)
         print()
         print(volume.xml.items())


        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")

        try:
         viewing = self['iq3'].get_viewing(self.jid, self.to, self.Resource)
         print()
         print(viewing.xml.items())


        except IqError as e:
         print("Error " + str(e))
        except IqTimeout:
         print("Timeout ")

# disable sending of pop up message as kills OSD on box
#        try:
#         pmsg = self['iq3'].set_message(self.jid, self.to, self.Resource)
#         print()
#         print(pmsg.xml.items())


#        except IqError as e:
#         print("Error " + str(e))
#        except IqTimeout:
#         print("Timeout ")



    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def currentcallback(self, from_jid, result):
       print("we got data %s from %s", str(result), from_jid)
       self.disconnect()



if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-t", "--to", dest="to", help="send to who?")
    optp.add_option("-r", "--resource", dest="resource", help="resource")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = EchoBot(opts.jid, opts.password, opts.to, opts.resource)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('iq3', module=iq3)


    # If you are connecting to Facebook and wish to use the
    # X-FACEBOOK-PLATFORM authentication mechanism, you will need
    # your API key and an access token. Then you'll set:
    # xmpp.credentials['api_key'] = 'THE_API_KEY'
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are connecting to MSN, then you will need an
    # access token, and it does not matter what JID you
    # specify other than that the domain is 'messenger.live.com',
    # so '_@messenger.live.com' will work. You can specify
    # the access token as so:
    # xmpp.credentials['access_token'] = 'THE_ACCESS_TOKEN'

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=False)
        print("Done")
    else:
        print("Unable to connect.")
