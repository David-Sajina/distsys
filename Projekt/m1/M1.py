import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()
@routes.get("/")
async def getAndDistribute(req):
    try:
        tasks = []
        async with aiohttp.ClientSession() as session:
            res = await session.get("http://M0:8080/getData")
            podaci = await res.json()
            tasks.append(asyncio.create_task(session.post("http://M2:8082/", json=podaci)))
            tasks.append(asyncio.create_task(session.post("http://M3:8083/", json=podaci)))
            t = asyncio.gather(*tasks)
            await t
            print("t", t)

        return web.json_response({"status": "works"}, status=200)
    except Exception as e:
        return web.json_response({"status": "fail", "message": str(e)}, status=500)


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
