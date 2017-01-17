
from sleekxmpp.xmlstream import ElementBase, ET


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

