import logging

from rich.logging import RichHandler
from rich.text import Text

import discord

# Configure root logging
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler = RichHandler(
    show_level=False,
    rich_tracebacks=True,
    tracebacks_show_locals=True,
    log_time_format=lambda dt: Text(dt.strftime("%X,%f")[:-3]),
    tracebacks_suppress=[discord],
)
logging.basicConfig(handlers=[handler], level=logging.INFO)
handler.setFormatter(formatter)
logging.Logger.root.addHandler(handler)
logging.Logger.root.setLevel(logging.DEBUG)

logger_dc1 = logging.getLogger("discord")
logger_dc1.setLevel(logging.DEBUG)


def get_logger(name=None):
    """Helper function to get a logger instance with the specified name."""
    return logging.getLogger(name if name else "rip_bot")
