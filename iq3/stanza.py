
from sleekxmpp.xmlstream import ElementBase, ET

class Current(ElementBase):

 namespace = "foxtel:iq"
 name = 'current_programme'
 plugin_attrib = 'current_programme'
 interfaces = set(('current_programme'))
 sub_interfaces = interfaces

 def plugin_init(self):
  self.description = "iq3 stanza"
  self.xep = "iq3"

 def get_current(self, jid=None, ifrom=None, resource=None):
    iq = self.xmpp.Iq()
    iq['to'] = tjid + "/" + resource
    iq['from'] = jid + "/" + resource
    iq['id'] = '12345'
    iq['type'] = 'get'
    iq['xml:lang'] = 'en'
    iq.enable('current_programme')

    #return iq.send(block=True, timeout=timeout,callback=callback, now=True)


class current_programme(ElementBase):

 namespace = "foxtel:iq"
 name = 'current_programme'
 plugin_attrib = 'current_programme'
 interfaces = set(('current_programme'))
 sub_interfaces = interfaces

class diagnostic_tuner(ElementBase):

 namespace = "foxtel:iq"
 name = 'diagnostic_tuner'
 plugin_attrib = 'diagnostic_tuner'
 interfaces = set(('diagnostic_tuner'))
 sub_interfaces = interfaces 

class current_viewing(ElementBase):
 namespace = "foxtel:iq"
 name = 'current_viewing'
 plugin_attrib = 'current_viewing'
 interfaces = set(('current_viewing','current_channel'))
 sub_interfaces = set(['current_channel'])


