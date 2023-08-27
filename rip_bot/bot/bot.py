from discord.ext.commands import Context, Bot
from discord import Intents
from rip_bot.repository import SchedulersRepository
from rip_bot.jobs import HorizontOtBossAlertStrategy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from rip_bot.utils import get_logger

logger = get_logger(__name__)


class DiscordBot(Bot):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)

    async def on_ready(self):
        logger.info("[bold green]Bot is ready.[/bold green]", extra={"markup": True})
        scheduler = AsyncIOScheduler()
        list_of_schedulers = (
            await SchedulersRepository().list_horizon_ot_scheduled_tasks()
        )
        logger.info(f"List of schedulers: {list_of_schedulers}")
        for command_data in list_of_schedulers:
            guild_id = command_data.guild_id
            channel_id = command_data.channel_id
            if command_data.command == "horizonotalertboss":
                strategy = HorizontOtBossAlertStrategy(bot=self)
                hours, minutes, seconds = strategy.schedule()
                scheduler.add_job(
                    strategy.execute,
                    "interval",
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds,
                    args=(guild_id, channel_id),
                )

        scheduler.start()

    async def on_command_error(self, ctx: Context[Bot], exception: Exception):
        logger.exception(
            f"An error ocurred while executing command {ctx.command}: {exception}"
        )
        await super().on_command_error(ctx, exception)
