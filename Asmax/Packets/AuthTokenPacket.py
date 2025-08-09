import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class AuthTokenPacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 1, 19))
        self.ws = ws

    def send_packet(self, token: str):
        payload = {
            "interactive": False,
            "token": token,
            "chatsSync": 0,
            "contactsSync": 0,
            "presenceSync": 0,
            "draftsSync": 0,
            "chatsCount": 0,
        }
        self.send(payload, self.ws)

class AuthTokenAnswerPacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        super().__init__(header, payload)

    def process(self, custom_data: dict):
        pass