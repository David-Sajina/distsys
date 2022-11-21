import aiohttp
import aiosqlite
import asyncio
import time
from aiohttp import web

routes = web.RouteTableDef()
temp = []
"""setup punchline"""
@routes.post("/filterJoke")
async def get_nes(request):
    try:
        req = await request.json()
        temp.append({"setup":req.get("setup")})
        temp.append({"punchline":req.get("punchline")})
        print(temp)
        return web.json_response({"Status": "ok","jokez":req}, status=200)
    except Exception as e:
        return web.json_response({"Status": "error"}, status=500)

app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8081)