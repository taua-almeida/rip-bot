from abc import ABC, abstractmethod, abstractproperty
from discord.ext.commands import Bot


class CommandSchedulerStategy(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    @abstractproperty
    def command(self) -> str:
        """This should return the associated command for the strategy."""
        pass

    @abstractmethod
    def schedule(self, time: tuple[int, int, int]):
        """
        Schedule a command to be executed at a specific time,
        where time is a tuple,
        where the first element is the hour, the second is the minute and the third is the second
        """
        pass

    @abstractmethod
    def execute(
        self,
        guild_id: int,
        channel_id: int,
        users_id: list[int] | None = None,
    ):
        pass
