import asyncio
import logging

from Asmax.Packets.SendMessage import SendMessagePacket, SendReplyMessagePacket, SendStickerPacket, SendReplyStickerPacket
from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class LinkInfo:
    def __init__(self, data: dict):
        self.type = data["link"]["type"]
        self.chatId = data["link"]["chatId"]
        self.message = Message(data['chatId'], data["link"]["message"], None)

class Message:
    def __init__(self, chatId: int, data: dict, conn):
        data["chatId"] = chatId
        self.chatId = chatId
        self.conn = conn
        self.sender = data['sender']
        self.id = data['id']
        self.time = data['time']
        self.text = data['text']
        self.type = data['type']
        self.attaches = data['attaches']
        if data.__contains__("link"):
            self.is_reply = True
            self.link = LinkInfo(data)
        else:
            self.is_reply = False

    async def answer(self, text: str):
        packet = SendMessagePacket(self.conn)
        packet.send_packet(self.chatId, text, True)

    async def answer_sticker(self, sticker_id: int):
        packet = SendStickerPacket(self.conn)
        packet.send_packet(self.chatId, sticker_id, True)

    async def reply(self, text: str):
        packet = SendReplyMessagePacket(self.conn)
        packet.send_packet(self.chatId, text, self.id, True)

    async def reply_sticker(self, sticker_id: int):
        packet = SendReplyStickerPacket(self.conn)
        packet.send_packet(self.chatId, sticker_id, self.id, True)

class ReceiveMessagePacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        logging.debug("message " + str(payload))
        super().__init__(header, payload)
        self.chatId = payload["chatId"]
        self.message = Message(self.chatId, payload['message'], payload['__conn'])
        self.ttl = payload['ttl']
        self.prevMessageId = payload['prevMessageId']

    def process(self, custom_data: dict):
        if self.message.text != "":
            asyncio.run(custom_data['message_func'](self.message))
        else:
            for attach in self.message.attaches:
                if custom_data.__contains__(attach["_type"].lower()+"_func"):
                    asyncio.run(custom_data[attach["_type"].lower()+"_func"](self.message))
