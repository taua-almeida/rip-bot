from typing import Optional
from rip_bot.models import HorizonOtModel
from rip_bot.database import DatabaseClient
from pydantic import BaseModel


class HorizonOtScheduledCommands(BaseModel):
    guild_id: Optional[int] = None
    channel_id: Optional[int] = None
    command: str


class SchedulersRepository:
    async def list_horizon_ot_scheduled_tasks(
        self,
    ) -> list[HorizonOtScheduledCommands] | None:
        async with DatabaseClient.get_client() as ctx:
            result = await ctx.execute(
                "select distinct command, guild_id, channel_id from horizonot_scheduler where active = ?",
                [True],
            )
            if not result or not result.rows:
                return None
            return [
                HorizonOtScheduledCommands(
                    command=row[0], guild_id=row[1], channel_id=row[2]
                )
                for row in result.rows
            ]
