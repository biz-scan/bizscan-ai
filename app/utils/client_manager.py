import httpx

class HttpClientManager:
    client: httpx.AsyncClient = None

    @classmethod
    async def start(cls):
        cls.client = httpx.AsyncClient(
            timeout=httpx.Timeout(100.0, connect=10.0),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )

    @classmethod
    async def stop(cls):
        if cls.client:
            await cls.client.aclose()
            cls.client = None