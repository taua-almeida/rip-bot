from discord.ext.commands import Context, Bot
from discord import Intents
from rip_bot.repository import SchedulersRepository
from rip_bot.utils import get_logger

logger = get_logger(__name__)


class DiscordBot(Bot):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)

    async def on_ready(self):
        logger.info("[bold green]Bot is ready.[/bold green]", extra={"markup": True})
        list_of_schedulers = (
            await SchedulersRepository().list_horizon_ot_scheduled_tasks()
        )
        logger.info(f"List of schedulers: {list_of_schedulers}")

    async def on_command_error(self, ctx: Context[Bot], exception: Exception):
        logger.exception(
            f"An error ocurred while executing command {ctx.command}: {exception}"
        )
        await super().on_command_error(ctx, exception)
