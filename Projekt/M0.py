import aiosqlite
import asyncio
from aiohttp import web
import aiofiles
import json

routes = web.RouteTableDef()

async def check_db():
    async with aiosqlite.connect("baza.db") as db:
        if (db):
            print("Baza spojena")
            """async with db.execute("DELETE FROM podaci"):
               await db.commit()"""
            async with db.execute("SELECT COUNT(*) FROM podaci") as cur:
                c = await cur.fetchall()
                print(c[0][0])
                await db.commit()
                if(c[0][0]==0):
                    print("prazna baza")
                    await fill_db()
        else:
            print("Error pri spajanju")

async def fill_db():
    async with aiofiles.open("datasetFile.json", mode="r") as file:
        max_num = 1
        i = 0
        print("filldb")
        async for cur in file:
            print(f"{round(i/max_num*100,0)}% done..")
            async with aiosqlite.connect("baza.db") as db:
                await db.execute(
                    "INSERT INTO podaci (username,ghlink,filename,content) VALUES (?,?,?,?)",
                    (json.loads(cur)["repo_name"].split("/")[0], "https://github.com/" + json.loads(cur)["repo_name"], json.loads(cur)["path"].split("/")[-1], json.loads(cur)["content"],),
                )
                await db.commit()
            i += 1
            if i == max_num:
                return

@routes.get("/getData")
async def getData(request):
    try:
        response = {
            "data": [],
        }
        async with aiosqlite.connect("baza.db") as db:
            async with db.execute("SELECT * FROM podaci ORDER BY RANDOM() LIMIT 100") as cur:
                async for row in cur:
                    response["data"].append({'id': row[0], 'username': row[1], 'ghlink': row[2], 'filename': row[3], 'content': row[4]})
                await db.commit()
        return web.json_response(response, status=200)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)}, status=500)

asyncio.run(check_db())
app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)