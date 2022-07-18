from httpx import AsyncClient

BASE_URL = "https://{host}/restconf/data"


class HTTPClient:
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.url = BASE_URL.format(host=host)
        self.client = AsyncClient(auth=(self.username, self.password), verify=False)

    async def close(self) -> None:
        return await self.client.aclose()
