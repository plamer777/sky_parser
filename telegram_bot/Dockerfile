FROM python:3.10-slim
WORKDIR /telegram_bot
RUN pip install telebot asyncio aiohttp
COPY . .
CMD python3 main.py
