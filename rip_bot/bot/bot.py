from discord.ext.commands import Context, Bot
from discord import Intents

import logging

logger = logging.getLogger(__name__)


class DiscordBot(Bot):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)

    async def on_command_error(self, ctx: Context[Bot], exception: Exception):
        logger.exception(
            f"An error ocurred while executing command {ctx.command}: {exception}"
        )
        await super().on_command_error(ctx, exception)
