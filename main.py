import logging

from Asmax.Max.Client import MaxClient
from Asmax.Packets.ReceiveMessage import Message


async def message_hand(message: Message):
    if message.text == "/start":
        await message.reply("Привет! я юзербот валлдева!")
    else:
        await message.reply_sticker(272821)

async def sticker_hand(message: Message, attach: dict):
    print("sticker")
    await message.reply(str(attach["stickerId"]))

logging.getLogger().setLevel(logging.DEBUG)
max_client = MaxClient("test_asmax")
max_client.handlers.add_message_handler(message_hand)
max_client.handlers.add_sticker_handler(sticker_hand)
max_client.loop()