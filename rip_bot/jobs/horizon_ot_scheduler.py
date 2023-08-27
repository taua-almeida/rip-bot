from rip_bot.repository import HorizontOtRepository
from rip_bot.scraping import HorizonOtScrape
from rip_bot.models import HorizonBossModel
from rip_bot.utils import get_logger
from discord import Embed
from .command_scheduler import CommandSchedulerStategy
from datetime import datetime

logger = get_logger(__name__)

from pprint import pprint


class HorizontOtBossAlertStrategy(CommandSchedulerStategy):
    @property
    def command(self) -> str:
        return "horizonotalertboss"

    async def _boss_check_alert(self) -> list[HorizonBossModel] | None:
        repo = HorizontOtRepository()
        horizonot_scapper = HorizonOtScrape()
        todays_bosses_check = await repo.list_today_boss_check(datetime.now().date())
        bosses = await horizonot_scapper.fetch_daily_bosses()
        if not todays_bosses_check:
            logger.info("Não há bosses checados hoje, criando...")
            if not bosses:
                logger.warning("Não foi possível encontrar os bosses de hoje")
                return None
            for boss in bosses:
                await repo.create_daily_boss_check(data=boss)
            return None

        new_borns: list[HorizonBossModel] = []
        for today_boss in todays_bosses_check:
            if today_boss.is_born:
                continue
            for boss in bosses:
                if boss.name == today_boss.name:
                    if boss.is_born:
                        logger.info(f"Boss {boss.name} is born")
                        new_borns.append(boss)
                        await repo.update_daily_boss_status(boss)

        return new_borns

    async def execute(self, guild_id: int, channel_id: int) -> None:
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)
        new_borns = await self._boss_check_alert()
        if not new_borns:
            return
        repo = HorizontOtRepository()
        users = await repo.list_all_command_alerts_active(self.command)
        if not users:
            return

        embeded_msg = Embed(
            title="HorizonOT Boss Alert!",
            color=0x00FF00,
        )

        embeded_msg.add_field(
            name="Atenção!",
            value=", ".join(users),
            inline=False,
        )

        for boss in new_borns:
            embeded_msg.add_field(
                name=f"🌟 O Boss: {boss.name}, nasceu!",
                value=f"**Born time: {boss.born_at}** \n **Wiki details: [Info]({boss.details})**",
                inline=False,
            )

        await channel.send(embed=embeded_msg)

    def schedule(self) -> tuple[int, int, int]:
        return (0, 1, 0)
