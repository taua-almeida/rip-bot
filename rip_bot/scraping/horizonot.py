from bs4 import BeautifulSoup
from datetime import datetime

from rip_bot.models import HorizonBossModel
from .client import HttpClient

from rip_bot.utils import get_logger

logger = get_logger(__name__)


class HorizonOtScrape:
    def __init__(self) -> None:
        self.base_url = "https://site.horizonot.com.br"
        self.headers = {
            "authority": "site.horizonot.com.br",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        self.client = HttpClient(base_url=self.base_url, headers=self.headers)
        self.thumbnail = "https://site.horizonot.com.br/layouts/tibiacom/images/header/tibia-logo-artwork-top.gif"

    def _is_boss_born(self, boss_born_status_msg: str) -> bool:
        if "Born at" in boss_born_status_msg:
            return True
        return False

    def _born_time(self, boss_born_status_msg: str) -> str | None:
        date_time_str = " ".join(boss_born_status_msg.split(", ")[1:3])
        try:
            date_time_obj = datetime.strptime(date_time_str, "%d/%m/%Y %H:%M:%S")
        except:
            logger.warning("Não foi possível converter a string para datetime")
            return None
        return date_time_obj

    async def fetch_daily_bosses(self) -> list[HorizonBossModel] | None:
        response = await self.client.fetch(
            endpoint="/", params={"subtopic": "checkboss"}
        )
        await self.client.close()
        parse_html = BeautifulSoup(response.text, "html5lib")
        parsed_html = parse_html.find_all(attrs={"id": "raidDays"})

        if not parse_html:
            logger.warning("Não foi possível encontrar o elemento no index HTML")
            return None

        daily_monsters_table: list = [
            result
            for element in parsed_html
            for result in element.find_all(attrs={"class": "TableContent"})
            if result
        ]

        if not daily_monsters_table:
            logger.warning("Não foi possível encontrar a tabela de bosses diários")
            return None

        boss_sections: list = [
            monster_section
            for daily_monsters in daily_monsters_table
            for monster_section in daily_monsters.find_all("tr")
            if monster_section
        ]

        bosses: list[HorizonBossModel] = []
        for boss in boss_sections:
            boss_data = boss.find_all("td")

            # Extract image
            relative_image_url = boss_data[0].find("img")["src"]
            corrected_image_url = relative_image_url.replace(".", "", 1).replace(
                " ", "%20"
            )
            boss_image = self.base_url + corrected_image_url

            # Extract name
            boss_name = boss_data[1].text

            # Check if boss is born
            boss_birth_text = boss_data[2].text
            boss_is_born = self._is_boss_born(boss_birth_text)

            # Extract born time if boss is born
            born_at_time = None
            if boss_is_born:
                born_at_time = self._born_time(boss_birth_text)

            # Extract details
            boss_details = boss_data[3].find("a")["href"]

            # Create boss object and append to bosses list
            bosses.append(
                HorizonBossModel(
                    name=boss_name,
                    image=boss_image,
                    is_born=boss_is_born,
                    born_at=born_at_time,
                    details=boss_details,
                    meta=boss.text,
                )
            )

        return bosses
