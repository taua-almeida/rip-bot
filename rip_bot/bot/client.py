from discord import Client, Intents
import logging

logger = logging.getLogger(__name__)


class DiscordBotClient(Client):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)

    async def on_ready(self):
        logger.info("[bold green]Bot is ready.[/bold green]", extra={"markup": True})
