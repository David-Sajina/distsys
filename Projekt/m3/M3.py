import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


@routes.post("/")
async def wt(request):
    try:
        print("hello")
        req = await request.json()
        print("got req")
        response = await sort(req)
        print(len(response))
        async with aiohttp.ClientSession() as session:
            res = await session.post("http://M4:8084/gatherData", json=response)
        print("posted", res)
        return web.json_response({"response": res}, status=200)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


async def sort(dic):
    entries = dic["data"]
    saved_data = []
    for entry in entries:
        if entry['username'].startswith('d'):
            saved_data.append(entry)
    return saved_data


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8083)
