# import datetime
# import logging
# import os
# import select
# import threading
# import time
# from contextlib import closing, contextmanager
#
# import psycopg2
# import requests
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#
# import odoo
# from odoo.tools import config
#
# # from .channels import ENQUEUED, NOT_DONE, PENDING, ChannelManager
#
# SELECT_TIMEOUT = 60
# ERROR_RECOVERY_DELAY = 5
#
# _logger = logging.getLogger(__name__)
#
#
# def _connection_info_for(db_name):
#     db_or_uri, connection_info = odoo.sql_db.connection_info_for(db_name)
#
#     # for p in ("host", "port", "user", "password"):
#     #     cfg = os.environ.get(
#     #         "ODOO_QUEUE_JOB_JOBRUNNER_DB_%s" % p.upper()
#     #     ) or queue_job_config.get("jobrunner_db_" + p)
#     #
#     #     if cfg:
#     #         connection_info[p] = cfg
#
#     return connection_info
#
#
# class Database(object):
#     def __init__(self, db_name):
#         print("====")
#         self.db_name = db_name
#         connection_info = _connection_info_for(db_name)
#         self.conn = psycopg2.connect(**connection_info)
#         self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#
#         self._initialize()
#
#     def close(self):
#         # pylint: disable=except-pass
#         try:
#             self.conn.close()
#         except Exception:
#             pass
#         self.conn = None
#
#     def _initialize(self):
#         print("_initialize")
#         with closing(self.conn.cursor()) as cr:
#             cr.execute("LISTEN mail_message_prosody_archive_processor")


from odoo import api, models
import psycopg2
import threading


class PostgreSQLListener:
    def __init__(self, config):
        self.notification_channel = 'mail_message_prosody_archive_processor'
        self.connection = None
        self.channel = None
        self.running = False
        self.config = config

    def init(self):
        self.connection = psycopg2.connect(
            dbname='xmpp-sexton.lvh.me',
            user='ayomir',
            password='xmpp',
            host='localhost',
            port=5432
        )
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.channel = self.connection.cursor()
        self.channel.execute(f"LISTEN {self.notification_channel};")
        self.running = True

        def listen_notifications():
            while self.running:
                self.connection.poll()
                while self.connection.notifies:
                    notification = self.connection.notifies.pop()
                    self.handle_notification(notification.payload)

        threading.Thread(target=listen_notifications).start()

    def handle_notification(self, payload):
        # Handle the received notification and extract the payload
        print("Received notification:", payload)

        # Example: Parse the payload as JSON
        import json
        payload_dict = json.loads(payload)
        print(payload_dict)
        # Access the individual values in the payload
        host = payload_dict.get('prosody_host')
        user = payload_dict.get('prosody_user')
        store = payload_dict.get('prosody_store')
        key = payload_dict.get('prosody_key')
        with_value = payload_dict.get('prosody_with')
        value = payload_dict.get('prosody_value')

        # Process the payload values as needed
        # ...
