# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, SUPERUSER_ID
import logging

logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # this is the trigger that sends messages when prosody message drops
    logger.info("Create prosody_archive_sync trigger")
    env.cr.execute(
        """
            DROP TRIGGER IF EXISTS prosody_archive_sync ON prosodyarchive;
            CREATE OR REPLACE
                FUNCTION prosody_archive_sync() RETURNS TRIGGER AS $$
            DECLARE
                payload TEXT;
            BEGIN
                INSERT INTO mail_message_prosody_archive_processor(
                    prosody_host,
                    prosody_user,
                    prosody_store,
                    prosody_key,
                    prosody_with,
                    prosody_value
                )
                VALUES(
                    NEW.host,
                    NEW.user,
                    NEW.store,
                    NEW.key,
                    NEW.with,
                    NEW.value
                );
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
            
            CREATE TRIGGER prosody_archive_sync
                AFTER INSERT OR UPDATE OR DELETE
                ON prosodyarchive
                FOR EACH ROW EXECUTE PROCEDURE prosody_archive_sync();
        """
    )
