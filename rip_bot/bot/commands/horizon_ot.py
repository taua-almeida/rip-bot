from datetime import date
from discord import Embed
from discord.ext.commands import Context, Cog, command
from rip_bot.scraping import HorizonOtScrape
from rip_bot.bot import DiscordBot


class HorizonOtCommands(Cog):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @command(
        name="horizonotdailybosses", help="Check today's bosses status in HorizonOT"
    )
    async def check_daily_bosses_status(self, ctx: Context[DiscordBot]) -> None:
        horizonot = HorizonOtScrape()
        bosses = await horizonot.fetch_daily_bosses()
        if not bosses:
            await ctx.send("Não foi possível encontrar os bosses de hoje")
            return

        current_date = date.today()
        weekday_name = current_date.strftime("%A")

        embeded_msg = Embed(
            title="HorizonOT Boss Check",
            description=f"**Today's ({weekday_name} - {current_date}) Bosses Status** {ctx.author.mention}",
            color=0x00FF00,
        )
        for boss in bosses:
            boss_status = "🔴 **Not Born**"
            if boss.is_born:
                boss_status = f"🟢 **Born at {boss.born_at}**"
            embeded_msg.add_field(
                name=f"**🌟 {boss.name}**",
                value=f"{boss_status} \n **Wiki details: [Info]({boss.details})** \n",
                inline=False,
            ).set_thumbnail(url=horizonot.thumbnail)

        await ctx.send(embed=embeded_msg)


async def setup(bot: DiscordBot):
    await bot.add_cog(HorizonOtCommands(bot))
