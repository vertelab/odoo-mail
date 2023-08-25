# import slixmpp
# from slixmpp.plugins import xep_0045
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
#
# class MUCBot(slixmpp.ClientXMPP):
#     def __init__(self, jid, password):
#         super().__init__(jid, password)
#         self.register_plugin("xep_0045")  # Register the xep_0045 plugin
#         self.add_event_handler("session_start", self.start)
#         self.add_event_handler("muc::{}::got_online".format(self.boundjid.bare), self.on_muc_online)
#
#     def start(self, event):
#         self.get_roster()
#         self.send_presence()
#         # Create a MUC room
#         muc_plugin = self.plugin["xep_0045"]
#         muc_plugin.join_muc("helloworld14@conference.rita.vertel.se", "john")
#
#     def on_muc_online(self, presence):
#         print("Room creation verified. Presence received: {}".format(presence))
#
#
# if __name__ == "__main__":
#     xmpp = MUCBot("john@rita.vertel.se", "john")
#     xmpp.connect()
#     xmpp.process()


import slixmpp
from slixmpp.plugins import xep_0045
import logging

# logging.basicConfig(level=logging.DEBUG)


class MUCBot(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("muc::{}::got_online".format(self.boundjid.bare), self.on_muc_online)

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        await self.create_and_configure_muc_room()

    async def create_and_configure_muc_room(self):
        room_name = "helloworld16"
        room_domain = "conference.rita.vertel.se"
        room_jid = f"{room_name}@{room_domain}"

        await self.plugin['xep_0045'].join_muc(room_jid, "demo")

        form = await self.plugin['xep_0045'].get_room_config(room_jid)
        form['muc#roomconfig_roomname'] = 'My Awesome Room'
        form['muc#roomconfig_publicroom'] = True

        await self.plugin['xep_0045'].set_room_config(room_jid, form)

    def on_muc_online(self, presence):
        print("Room creation verified. Presence received: {}".format(presence))


if __name__ == "__main__":
    xmpp = MUCBot("demo@rita.vertel.se", "demo")
    xmpp.register_plugin('xep_0045')  # Register the xep_0045 plugin
    xmpp.connect()
    xmpp.process()
