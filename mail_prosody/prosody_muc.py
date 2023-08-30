# import slixmpp
# from slixmpp.plugins import xep_0045
# import logging
# import asyncio
#
# logging.basicConfig(level=logging.DEBUG)
#
#
# class MUCBot(slixmpp.ClientXMPP):
#     def __init__(self, jid, password):
#         super().__init__(jid, password)
#         self.add_event_handler("session_start", self.start)
#         self.add_event_handler("muc::{}::got_online".format(self.boundjid.bare), self.on_muc_online)
#
#     async def start(self, event):
#         await self.get_roster()
#         self.send_presence()
#         await self.create_and_configure_muc_room()
#
#     async def create_and_configure_muc_room(self):
#         room_name = "helloworld"
#         room_domain = "conference.rita.vertel.se"
#         room_jid = f"{room_name}@{room_domain}"
#
#         await self.plugin['xep_0045'].join_muc(room_jid, "admin")
#
#         form = await self.plugin['xep_0045'].get_room_config(room_jid)
#         form['muc#roomconfig_roomname'] = 'Hello World Room'
#         form['muc#roomconfig_publicroom'] = True
#         form['muc#roomconfig_persistentroom'] = True  # Set the room as persistent
#
#         await self.plugin['xep_0045'].set_room_config(room_jid, form)
#         print("Room creation and configuration complete.")
#
#         await asyncio.sleep(2)  # Wait for a moment to allow presence updates to be processed
#
#         loop = asyncio.get_event_loop()
#         loop.stop()  # Stop the event loop to end the script
#
#     def on_muc_online(self, presence):
#         print("Room creation verified. Presence received: {}".format(presence))
#
#
# if __name__ == "__main__":
#     xmpp = MUCBot("admin@rita.vertel.se", "admin")
#     xmpp.register_plugin('xep_0045')  # Register the xep_0045 plugin
#     xmpp.connect()
#     xmpp.process()


import slixmpp
from slixmpp.plugins import xep_0045
import argparse
import logging
import ast
import asyncio
import json

# logging.basicConfig(level=logging.DEBUG)


class MUCBot(slixmpp.ClientXMPP):
    def __init__(self, options_dict):
        self.options_dict = options_dict
        super().__init__(self.options_dict.get("jid", ""), self.options_dict.get("password", ""))

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("muc::{}::got_online".format(self.options_dict.get("jid", "")), self.on_muc_online)

    async def start(self, event):
        self.options_dict["jid"] = self.boundjid.full  # Store the full JID
        await self.get_roster()
        self.send_presence()
        await self.create_and_configure_muc_room()

    async def create_and_configure_muc_room(self):
        await self.plugin['xep_0045'].join_muc(
            self.options_dict.get("room_jid", ""), self.options_dict.get("nickname", ""))

        form = await self.plugin['xep_0045'].get_room_config(self.options_dict.get("room_jid", ""))

        # Update the 'muc#roomconfig_roomname' field
        for field in form['fields']:
            if field['var'] == 'muc#roomconfig_roomname':
                field['value'] = self.options_dict.get("room_name", "")
                break

        # Update the 'muc#roomconfig_roomdesc' field
        for field in form['fields']:
            if field['var'] == 'muc#roomconfig_roomdesc':
                field['value'] = self.options_dict.get("room_desc", "")
                # field['value'] = f"{self.options_dict.get('room_desc', '')} -odoo"
                break

        # Update the 'muc#roomconfig_persistentroom' field
        for field in form['fields']:
            if field['var'] == 'muc#roomconfig_persistentroom':
                field['value'] = '1'
                break

        # Update the 'muc#roomconfig_publicroom' field
        for field in form['fields']:
            if field['var'] == 'muc#roomconfig_publicroom':
                field['value'] = '1'
                break

        # Update the 'muc#roomconfig_roomsecret' field
        for field in form['fields']:
            if field['var'] == 'muc#roomconfig_roomsecret':
                field['value'] = self.options_dict.get("room_password", "")
                break

        await self.plugin['xep_0045'].set_room_config(self.options_dict.get("room_jid", ""), form)
        print("Room creation and configuration complete.")

        await asyncio.sleep(2)  # Wait for a moment to allow presence updates to be processed

        loop = asyncio.get_event_loop()
        loop.stop()  # Stop the event loop to end the script

    def on_muc_online(self, presence):
        print("Room creation verified. Presence received: {}".format(presence))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and configure a MUC room")
    parser.add_argument("--options", type=str, help="Dictionary of options as a string")
    args = parser.parse_args()

    # options_dict = json.loads(args.options) if args.options else {}
    options_dict = ast.literal_eval(args.options) if args.options else {}

    xmpp = MUCBot(options_dict)
    xmpp.register_plugin('xep_0045')  # Register the xep_0045 plugin
    xmpp.connect()
    xmpp.process()
