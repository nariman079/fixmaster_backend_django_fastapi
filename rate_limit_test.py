import asyncio

from aiohttp import ClientSession


async def send_requests():
    async with ClientSession() as session:
        async with session.get("http://localhost:8000/api/test/") as response:
            status_code = response.status
            print(status_code)
async def main():
    tasks = [asyncio.create_task(send_requests()) for _ in range(10)]
    await asyncio.gather(*tasks)


asyncio.run(main())