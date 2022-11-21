import aiohttp
import aiosqlite
import asyncio
import time
from aiohttp import web
"""Kreiraj 4 web servisa. Prvi servis sastoji se od jedne rute (/getJokes). Unutar
te rute šalje se 6 puta po 10 zahtjeva na sljedeća dva URL-a :
https://official-joke-api.appspot.com/random_joke
https://randomuser.me/api/"""
routes = web.RouteTableDef()


@routes.get("/getJokes")
async def get_jokes(request):
        try:
            tasks = []
            tasks2 = []
            jokes = []
            persons = []
            async with aiohttp.ClientSession() as session:
                for _ in range(1):
                    for i in range(2):
                        tasks.append(asyncio.create_task(session.get("https://official-joke-api.appspot.com/random_joke")))
                        tasks2.append(asyncio.create_task(session.get("https://randomuser.me/api/")))
                        res = await asyncio.gather(*tasks)
                        res2 = await asyncio.gather(*tasks2)
                        res = [await x.json() for x in res]
                        res2 = [await y.json() for y in res2]
                        x = asyncio.create_task(sendJokes(res, session))
                        y = asyncio.create_task(sendPerson(res2, session))
                        await x
                        await y
            return web.json_response({"Status": "ok","message": res,"person":res2}, status=200)
        except Exception as e:
            return web.json_response({"Status S1": "error"}, status=500)

async def sendJokes(json_data, session):
    for i in range(len(json_data)):
        async with session.post("http://0.0.0.0:8081/sendJokes", json=json_data[i]) as response:
            print("Sending",json_data[i])
            x = await response.text()
    return x


async def sendPerson(json_data, session):
    for i in range(len(json_data)):
        async with session.post("http://0.0.0.0:8082/sendPerson", json=json_data[i]) as response:
            print("Sending",json_data[i])
            x = await response.text()
    return x

app = web.Application()

app.router.add_routes(routes)

web.run_app(app)