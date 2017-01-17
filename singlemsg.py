#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

"""
    Project Scorpio XMPP boxymcboxface control

    This file is used to login and send commands then log off.
    Mainly for testing

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


class Scorpio(sleekxmpp.ClientXMPP):

    """
    Simple Clkass to login send cmds and log out
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


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.
        """

        self.send_presence()
        self.get_roster()

        #
        try:
            current = self['iq3'].get_current(self.jid, self.to, self.Resource)
            #print(current['programme']['event_length'])
            print("THIS IS WHAT I AM PRINTING:")
            print(current)
        except IqError as e:
            print("Error " + e)
        except IqTimeout:
            print("Timeout ")
        #
        # try:
        #     diag = self['iq3'].get_diag(self.jid, self.to, self.Resource)
        #     print()
        #     print(diag.xml.items())
        #
        #
        # except IqError as e:
        #     print("Error " + e)
        # except IqTimeout:
        #     print("Timeout ")
        #
        # try:
        #     channel = self['iq3'].set_viewing(self.jid, self.to, self.Resource)
        #     print()
        #     print(channel.xml.items())
        #
        # except IqError as e:
        #     print("Error " + e)
        # except IqTimeout:
        #     print("Timeout ")

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
    xmpp = Scorpio(opts.jid, opts.password, opts.to, opts.resource)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
#    xmpp.register_plugin('xep_0060') # PubSub
#    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('iq3', module=iq3)


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
