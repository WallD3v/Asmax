import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class AuthPacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 5, 17))
        self.ws = ws

    def send_packet(self, phone_number: str):
        payload = {
            "phone": phone_number,
            "type": "START_AUTH",
            "language": MaxUtils.lang_code
        }
        self.send(payload, self.ws)

class AuthAnswerPacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        super().__init__(header, payload)
        self.requestMaxDuration = self.payload["requestMaxDuration"]
        self.requestCountLeft = self.payload["requestCountLeft"]
        self.altActionDuration = self.payload["altActionDuration"]
        self.codeLength = self.payload["codeLength"]
        self.token = self.payload["token"]

    def process(self, custom_data: dict):
        custom_data["return_method"](input("Enter code >"), self.token)