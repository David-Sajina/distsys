import aiosqlite
import asyncio
from aiohttp import web
import aiofiles
import json
import os

routes = web.RouteTableDef()
entry = []


async def write_files():
    # Create the "files" directory if it does not exist
    if not os.path.exists('files'):
        os.makedirs('files')
        
    print("write")
    for data in entry:
        filename = data['filename']
        content = data['content']
        async with aiofiles.open(f'files/{filename}', 'w', encoding='utf-8') as f:
            await f.write(content)


@routes.post("/gatherData")
async def gather_data(request):
    req = await request.json()
    print("got data")
    print(req)
    entry.extend(req)
    print(len(entry))
    if len(entry) > 10:
        await write_files()

    return web.json_response(
        {
            "status": "ok",
        },
        status=200,
    )


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8084)
