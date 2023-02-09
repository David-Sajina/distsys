from aiohttp import web
import random
import asyncio
import aiohttp
import logging
import subprocess


logging.basicConfig(format='%(asctime)s -> %(message)s', datefmt='%d/%m/%Y - %H:%M:%S', level=logging.INFO)

M = 1000
numRequest = 0
numResponse = 0
tasksCounter = 0

randWorkers = random.randint(5, 10)
subprocess.call(r"RUN_WORKERS.BAT") #COMMENT THIS IF YOU WANT TO MANUALY RUN WORKERS OR THEY ARE ALREADY RUNNING

workers = {"Worker" + str(id): [] for id in range(1, randWorkers+1)}
routes = web.RouteTableDef()


@routes.get("/")
async def function(request):
    try:
        global randWorkers, workers, M
        global numResponse, numRequest
        global tasksCounter

        numRequest += 1
        logging.info(f"Got new request! I recieved {numRequest} in total.")
        data = await request.json()
        codelen = len(data.get("codes"))

        code = '\n'.join(data.get("codes"))
        code_split = code.split("\n")
        codes_grouped = []
        for i in range(0, len(code_split), M):
            codes_grouped.append("\n".join(code_split[i:i+M]))
        data["codes"] = codes_grouped

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            curr_worker_ID = 1
            tasks = [asyncio.create_task(session.get(f"http://127.0.0.1:{8080 + curr_worker_ID}/", json={"id": data.get("client"), "data": code}))for code in data["codes"]]
            for task in tasks:
                workers[f"Worker{curr_worker_ID}"].append(task)
                curr_worker_ID = (curr_worker_ID + 1) % randWorkers + 1

            results = await asyncio.gather(*tasks)
            tasksCounter += len(results)
            results = [await result.json() for result in results]
            results = [result.get("wordsCount") for result in results]

        numResponse += 1
        logging.info("Sent response.")
        logging.info(f"Status: {numResponse} responses and {tasksCounter} done tasks! {sum(results)}")

        return web.json_response({"client": data.get("client"), "results": results, "avg": round(sum(results) / codelen, 2)})
    except Exception as e:
        return web.json_response({"error": str(e)})


app = web.Application(client_max_size=1024 * 1024 * 100)

app.router.add_routes(routes)

web.run_app(app, port=8080, access_log=None)
