import os
from typing import List

from environs import Env
from flask import Flask
from she_logging.logging import logging

SYSTEM_UUIDS: List[str] = [
    "dhos-async-adapter",
    "dhos-robot",
    "dhos-services-api",
    "dhos-services-adapter-worker",
    "system",
]

# Disable NEOBOLT DEBUG logs unless specifically enabled.
NEOBOLT_LOG_LEVEL = os.environ.get("NEOBOLT_LOG_LEVEL", "INFO")
logging.getLogger("neobolt").setLevel(NEOBOLT_LOG_LEVEL)


class Configuration:
    env = Env()
    GDM_SMS_SENDER: str = env.str("GDM_SMS_SENDER", "GDm-Health")
    GDM_LINK_MSG: str = env.str(
        "GDM_LINK_MSG",
        "You can download the free GDm-Health app now, click "
        "https://intercom.help/medopad-ltd/en/collections/3678855-gdm-health-for-patients",
    )

    # If env var NEO4J_DB_URL is set, then we are using neo4j.
    NEO4J_ENABLED = bool(env.str("NEO4J_DB_URL", default="localhost"))
    NEO4J_DATABASE_URI: str = "{proto}://{auth}:{password}@{url}:{port}".format(
        proto=env.str("NEO4J_DB_PROTO", default="bolt"),
        url=env.str("NEO4J_DB_URL", default="localhost"),
        auth=env.str("NEO4J_DB_USERNAME", default="neo4j"),
        password=env.str("NEO4J_DB_PASSWORD", default="neo"),
        port=env.int("NEO4J_DB_PORT", default=7687),
    )
    DHOS_USERS_API_HOST = env.str("DHOS_USERS_API_HOST")
    JWT_EXPIRY_IN_SECONDS: int = env.int("JWT_EXPIRY_IN_SECONDS", 86400)


def init_config(app: Flask) -> None:
    app.config.from_object(Configuration)
