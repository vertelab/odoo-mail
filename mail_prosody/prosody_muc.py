import slixmpp
from slixmpp.plugins import xep_0045
import logging

logging.basicConfig(level=logging.DEBUG)


class MUCBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.register_plugin("xep_0045")  # Register the xep_0045 plugin
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("muc::{}::got_online".format(self.boundjid.bare), self.on_muc_online)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        # Create a MUC room
        muc_plugin = self.plugin["xep_0045"]
        muc_plugin.join_muc("helloworld2@conference.rita.vertel.se", "admin")

    def on_muc_online(self, presence):
        print("Room creation verified. Presence received: {}".format(presence))


if __name__ == "__main__":
    xmpp = MUCBot("admin@rita.vertel.se", "admin")
    xmpp.connect()
    xmpp.process()
