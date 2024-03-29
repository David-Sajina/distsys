from aiohttp import web
import random
import asyncio
import re
import string
import sys

print('cmd entry:', sys.argv)

routes = web.RouteTableDef()
print(type(sys.argv[1]), sys.argv[1])
#x = sys.argv[0].toString()
x = int(sys.argv[1])
@routes.get("/")
async def function(request):
	try:
		await asyncio.sleep(random.uniform(0.1, 0.3))

		data = await request.json()
		all_words = re.sub(f"[{string.punctuation}]", "", data.get("data")).split()
		all_words = len(all_words)

		await asyncio.sleep(random.uniform(0.1, 0.3))

		return web.json_response({"wordsCount": all_words}, content_type='application/json')
	except Exception as e:
		return web.json_response({"error": str(e)})

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port= x)
