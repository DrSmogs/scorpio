from sleekxmpp.plugins.base import register_plugin, BasePlugin

from iq3.stanza import current_programme, diagnostic_tuner, current_viewing
from iq3.current import iq3


register_plugin(iq3)
