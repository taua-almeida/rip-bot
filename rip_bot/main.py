import config
from rip_bot.bot import DiscordBot
import asyncio
from rip_bot.utils import get_logger
import libsql_client

logger = get_logger(__name__)


async def init_db():
    async with libsql_client.create_client(
        url=config.DB_URL, auth_token=config.DB_AUTH_TOKEN
    ) as client:
        await client.batch(
            [
                """ 
                CREATE TABLE IF NOT EXISTS horizonot_scheduler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_id INTEGER NOT NULL,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    command TEXT NOT NULL,
                    active BOOLEAN NOT NULL
                )
                """
            ]
        )


async def start_bot():
    bot = DiscordBot(command_prefix="$")

    await init_db()

    async with bot:
        await bot.load_extension("bot.commands.horizon_ot")
        logger.info("[green]Starting bot.[/green]", extra={"markup": True})
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        logger.warning(
            "[red]Bot has stopped due to keyboard interrupt.[/red]",
            extra={"markup": True},
        )
    except Exception as e:
        logger.error(f"[red]Error: {e}[/red]", extra={"markup": True})
    finally:
        loop.close()
