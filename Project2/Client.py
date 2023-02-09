import asyncio
import aiohttp
import pandas as pd

avg_total = 0
counter = 0
ClientsNum = 1000 #CHANGE TO HOW MANY CLIENTS YOU WANT!
id_s = list(range(1, ClientsNum))

print("Loading...")
df = pd.read_json("datasetFile.json", lines=True)
print("Loaded, creating tasks!")
client_rows = len(df) // len(id_s)
client = {id_: df.iloc[id_*client_rows:(id_+1)*client_rows]["content"].tolist() for id_ in id_s}

async def process_code():
    global avg_total, counter
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.create_task(session.get("http://127.0.0.1:8080/", json={"client": id_, "codes": codes})) for id_, codes in client.items()]
        print("Client.py is waiting for results...")
        taskres = await asyncio.gather(*tasks)
        taskres = [await x.json() for x in taskres]
        return taskres

resp = asyncio.run(process_code())

for r in resp:
    if 'client' in r:
        counter +=1
        avg_total += r['avg']
        print(f"Average length for client({r['client']}) is -> {r['avg']}")
    else:
        print(f"No 'client' key found in response: {r}")
print(f"Average length of all clinets is {round(avg_total/counter, 2)}")
