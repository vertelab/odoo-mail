import slixmpp
from slixmpp.plugins import xep_0045
import argparse
import logging
import ast
import asyncio
import json


logging.basicConfig(level=logging.DEBUG)


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
        await self.send_message()

    async def send_message(self):
        msg = self.Message()
        msg["to"] = self.options_dict.get("room_jid")
        msg["type"] = self.options_dict.get("type")
        msg["body"] = self.options_dict.get("message")
        msg.send()

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
