import config
from rip_bot.bot import DiscordBot
import asyncio
from rip_bot.utils import get_logger

logger = get_logger(__name__)


async def start_bot():
    bot = DiscordBot(command_prefix="$")

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
