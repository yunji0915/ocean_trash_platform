import telegram
import asyncio

TELEGRAM_TOKEN = 'YOUR_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
bot = telegram.Bot(token=TELEGRAM_TOKEN)

async def send_image(file_path, caption="탐지됨"):
    with open(file_path, 'rb') as f:
        await bot.send_photo(chat_id=CHAT_ID, photo=f, caption=caption)

async def send_image_with_location(file_path, map_path):
    await send_image(file_path)
    await send_image(map_path, caption="현재위치\n위도:35.157\n경도:129.163")
