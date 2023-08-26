from typing import Optional
from datetime import date
from discord import Embed
from discord.ext.commands import Context, Cog, command
from rip_bot.scraping import HorizonOtScrape
from rip_bot.bot import DiscordBot
from rip_bot.repository import HorizontOtRepository
from rip_bot.models import HorizonOtModel


class HorizonOtCommands(Cog):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot
        self.horizonot_repository = HorizontOtRepository()

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
            description=f"**Here are today's ({weekday_name} - {current_date}) Bosses Status** {ctx.author.mention}",
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

    @command(
        name="horizonotalertboss",
        help=(
            "Alert when a boss is born in HorizonOT,\
            use $horizonotalertboss start to start the alert and $horizonotalertboss stop to stop the alert,\
            use $horizonotalertboss list to list users with alert on "
        ),
    )
    async def alert_boss(
        self, ctx: Context[DiscordBot], *, message: Optional[str]
    ) -> None:
        if message == "list":
            users = await self.horizonot_repository.list_all_command_alerts_active(
                command=ctx.command.name
            )
            if len(users) == 0:
                await ctx.send("Nenhum usuário com alerta ativo")
            await ctx.send("Usuários com alerta ativo: " + ", ".join(users))
            return

        data = HorizonOtModel(
            author_id=ctx.author.id,
            guild_id=ctx.guild.id,
            channel_id=ctx.channel.id,
            command=ctx.command.name,
            active=True,
        )

        is_user_alerting: tuple | None = (
            await self.horizonot_repository.get_user_alerting(data)
        )

        if is_user_alerting:
            if is_user_alerting[1]:
                await ctx.send(
                    "Usuário já está com alerta ativo... \nDesativando alerta..."
                )
                deactivated = await self.horizonot_repository.deactivate_scheduler(
                    author_id=ctx.author.id,
                    guild_id=ctx.guild.id,
                    channel_id=ctx.channel.id,
                    command=ctx.command.name,
                )
                if not deactivated:
                    await ctx.send("Não foi possível desativar o alerta")

                await ctx.send(
                    f"{ctx.author.mention} seu alerta foi desativado com sucesso"
                )
                return
            else:
                await ctx.send(
                    "Usuárioestá com alerta invativo... \n Ativando alerta..."
                )
                activated = await self.horizonot_repository.activate_scheduler(
                    author_id=ctx.author.id,
                    guild_id=ctx.guild.id,
                    channel_id=ctx.channel.id,
                    command=ctx.command.name,
                )
                if not activated:
                    await ctx.send("Não foi possível ativar o alerta")
                    return

                await ctx.send(
                    f"{ctx.author.mention} seu alerta foi ativado com sucesso"
                )
                return

        is_alert_created = await self.horizonot_repository.create_scheduler(data)
        if not is_alert_created:
            await ctx.send("Não foi possível criar o alerta")
            return
        await ctx.send(f"{ctx.author.mention} seu alerta foi criado com sucesso")


async def setup(bot: DiscordBot):
    await bot.add_cog(HorizonOtCommands(bot))
