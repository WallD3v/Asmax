import asyncio
import logging
import os
import threading

from websocket import create_connection

from Asmax.Max.Connection import MaxConnection
from Asmax.Max.Handlers import MaxHandlers

from Asmax.Packets.AuthPacket import AuthPacket, AuthAnswerPacket
from Asmax.Packets.AuthTokenPacket import AuthTokenPacket, AuthTokenAnswerPacket
from Asmax.Packets.ReceiveMessage import ReceiveMessagePacket, Message
from Asmax.Packets.SendCode import SendCodePacket, SendCodeAnswerPacket
from Asmax.Packets.SkipPacket import SkipPacket
from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.PreparePacket import PreparePacket, PrepareAnswerPacket
from Asmax.Utils.MaxUtils import MaxUtils


class MaxClient:
    def get_token(self):
        if os.path.isfile(self.session_name + ".max"):
            f = open(self.session_name + ".max")
            token = f.read()
            f.close()
            return token
        else:
            return None

    def set_token(self, token: str):
        self.token = token
        f = open(self.session_name + ".max", "w")
        f.write(token)
        f.close()

    def __init__(self, session_name: str, server: str = "wss://ws-api.oneme.ru/websocket", anonymous: bool = False):
        self.server = server
        self.session_name = session_name
        self.token = self.get_token()
        self.anonymous = anonymous
        self.handlers = MaxHandlers()

    def connect(self):
        self.ws = create_connection(self.server)
        self.conn = MaxConnection(self.ws)
        process_t = threading.Thread(target=self.conn.process)
        process_t.start()
        receive_t = threading.Thread(target=self.conn.receive_packets)
        receive_t.start()
        # Skipping packets
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 1, -1, 64), SkipPacket)  # AddLocalMessage
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 0, -1, 150), SkipPacket)  # AddedStickerToRecent
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 0, -1, 130), SkipPacket)  # idk
        # Needed packets
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 1, -1, 6), PrepareAnswerPacket)
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 1, -1, 17), AuthAnswerPacket,
                                  {"return_method": self.send_code})
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 1, -1, 18), SendCodeAnswerPacket,
                                  {"return_method": self.set_token})
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 1, -1, 19), AuthTokenAnswerPacket)
        self.conn.register_packet(PacketHeader(MaxUtils.global_ver, 0, -1, 128), ReceiveMessagePacket,
                                  {"message_func": self.handlers.process_message,
                                   "sticker_func": self.handlers.process_sticker})
    def start(self):
        self.connect()
        asyncio.run(self.start_async())

    def loop(self):
        while True:
            self.start()
            while self.conn.conn.connected:
                pass
            logging.warning("Reconnecting...")

    async def start_async(self):
        await self.prepare()
        if self.token is None:
            await self.auth("+7" + input("enter phone number: +7"))
        await self.auth_by_token()

    async def prepare(self):
        packet = PreparePacket(self.ws)
        if self.anonymous:
            packet.send_packet(MaxUtils.platform, MaxUtils.lang_code, MaxUtils.lang_code, "Unknown", "Unknown", MaxUtils.random_useragent(1), MaxUtils.global_web_version, MaxUtils.screen, MaxUtils.timezone)
        else:
            packet.send_packet(MaxUtils.platform, MaxUtils.lang_code, MaxUtils.lang_code, "Python", "MaxClient", MaxUtils.random_useragent(1), MaxUtils.global_web_version, MaxUtils.screen, MaxUtils.timezone)

    async def auth(self, phone_number: str):
        packet = AuthPacket(self.ws)
        packet.send_packet(phone_number)

    def send_code(self, code: str, token: str):
        packet = SendCodePacket(self.ws)
        packet.send_packet(code, token)

    async def auth_by_token(self):
        packet = AuthTokenPacket(self.ws)
        packet.send_packet(self.token)