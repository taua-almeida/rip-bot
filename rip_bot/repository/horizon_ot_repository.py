from rip_bot.database import DatabaseClient
from rip_bot.models import HorizonOtModel


class HorizontOtRepository:
    async def create_scheduler(self, data: HorizonOtModel) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "insert into horizonot_scheduler values (:id, :author_id, :guild_id, :channel_id, :command, :active)",
                data.model_dump(),
            )
            if not result:
                return None
            return result.last_insert_rowid

    async def get_user_alerting(
        self, discord_data: HorizonOtModel
    ) -> tuple[int, bool] | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "select id, active from horizonot_scheduler where author_id = ? and guild_id = ? and command = ?",
                [discord_data.author_id, discord_data.guild_id, discord_data.command],
            )
            if result and result.rows:
                for row in result.rows:
                    return row
            return None

    async def deactivate_scheduler(
        self, author_id: int, guild_id: int, channel_id: int, command: str
    ) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "update horizonot_scheduler set active = false where author_id = ? and guild_id = ? and channel_id = ? and command = ?",
                [author_id, guild_id, channel_id, command],
            )
            if not result:
                return None
            return result.last_insert_rowid

    async def activate_scheduler(
        self, author_id: int, guild_id: int, channel_id: int, command: str
    ) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "update horizonot_scheduler set active = true where author_id = ? and guild_id = ? and channel_id = ? and command = ?",
                [author_id, guild_id, channel_id, command],
            )
            if not result:
                return None
            return result.last_insert_rowid

    async def list_all_command_alerts_active(self, command: str) -> list[str]:
        users_actives = []
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "select author_id from horizonot_scheduler where command = ? and active = ?",
                [command, True],
            )
            if result and result.rows:
                for row in result.rows:
                    users_actives.append(f"<@{row[0]}>")
            return users_actives
