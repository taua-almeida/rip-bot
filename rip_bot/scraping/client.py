from typing import Any, Mapping, Optional

from httpx import AsyncClient, Headers, QueryParams, Response


class HttpClient:
    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Headers] = None,
        timeout: float = 10.0,
    ):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.client = AsyncClient(base_url=self.base_url, headers=self.headers)

    async def fetch(
        self,
        endpoint="",
        params: Optional[QueryParams] = None,
        data: Optional[Mapping[str, Any]] = None,
    ) -> Response:
        url = f"{self.base_url}{endpoint}"
        response = await self.client.request(
            "GET", url, params=params, data=data, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()
