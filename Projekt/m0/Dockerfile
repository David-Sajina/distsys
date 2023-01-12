FROM python:3.9

RUN pip install aiosqlite asyncio aiohttp aiofiles

COPY baza.db ./

COPY M0.py ./

CMD ["python", "./M0"]
