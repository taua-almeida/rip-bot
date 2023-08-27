from rip_bot.database import DatabaseClient
from rip_bot.models import HorizonOtModel, HorizonBossModel
from datetime import date


class HorizontOtRepository:
    async def create_scheduler(self, data: HorizonOtModel) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "insert into horizonot_scheduler (author_id, guild_id, channel_id, command, active) values (:author_id, :guild_id, :channel_id, :command, :active)",
                data.model_dump(exclude={"id"}),
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
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "select author_id from horizonot_scheduler where command = ? and active = ?",
                [command, True],
            )
            if result and result.rows:
                return [row[0] for row in result.rows]
            return []

    async def list_today_boss_check(self, today: date) -> list[HorizonBossModel] | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "select * from horizonot_boss_checker where date(checked_at / 1000, 'unixepoch') = ?",
                [today.strftime("%Y-%m-%d")],
            )
            if result and result.rows:
                bosses: list[HorizonBossModel] = []
                for row in result.rows:
                    bosses.append(HorizonBossModel(**row.asdict()))
                return bosses
            return None

    async def create_daily_boss_check(self, data: HorizonBossModel) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "insert into horizonot_boss_checker (name, image, is_born, born_at, details, meta, checked_at) values (?, ?, ?, ?, ?, ?, ?)",
                [
                    data.name,
                    data.image,
                    data.is_born,
                    data.born_at,
                    data.details,
                    data.meta,
                    data.checked_at,
                ],
            )
            if not result:
                return None
            return result.last_insert_rowid

    async def update_daily_boss_status(self, data: HorizonBossModel) -> int | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "update horizonot_boss_checker set is_born = ?, checked_at = ?  where name = ?",
                [data.is_born, data.checked_at, data.name],
            )
            if not result:
                return None
            return result.last_insert_rowid
