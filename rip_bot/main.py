import config
from rip_bot.bot import DiscordBot
import asyncio
from rip_bot.utils import get_logger
from rip_bot.database import DatabaseClient

logger = get_logger(__name__)


async def init_db():
    async with DatabaseClient.get_client() as client:
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
                """,
                """ 
                CREATE TABLE IF NOT EXISTS horizonot_boss_checker (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    image TEXT,
                    is_born BOOLEAN NOT NULL,
                    born_at DATETIME,
                    details TEXT,
                    meta TEXT NOT NULL
                )
                """,
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
