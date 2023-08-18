import os

from discord import Client, Intents, Member
from discord.ext.commands import Context, Bot

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.all()


class BotClient(Client):
    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_member_join(self, member: Member):
        await member.create_dm()
        await member.dm_channel.send(
            f"Oi {member.name}, bem vindo ao RIP, cuidado com chupacu!"
        )


client = BotClient(intents=intents)
bot = Bot(command_prefix="$", intents=intents)


@bot.command(name="otbosscheck", help="Check today's boss in HorizonOT")
async def ot_bosscheck(ctx: Context):
    await ctx.send("Today's boss is: Ferumbras")


bot.run(TOKEN)
