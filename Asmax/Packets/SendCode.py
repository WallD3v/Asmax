import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class SendCodePacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 18, 18))
        self.ws = ws

    def send_packet(self, code: str, token: str):
        payload = {
            "token": token,
            "verifyCode": code,
            "authTokenType": "CHECK_CODE"
        }
        self.send(payload, self.ws)

class TokenAttrs:
    def __init__(self, data: dict):
        is_register = data.__contains__("REGISTER")
        if is_register:
            self.token = data["REGISTER"]['token']
        else:
            self.token = data["LOGIN"]['token']

class Contact:
    def __init__(self, data: dict):
        self.accountStatus = data["accountStatus"]
        self.names = data["names"]
        self.phone = data["phone"]
        self.updateTime = data["updateTime"]
        self.id = data["id"]

class Profile:
    def __init__(self, data: dict):
        self.contact = Contact(data['contact'])

class SendCodeAnswerPacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        super().__init__(header, payload)
        self.tokenAttrs = TokenAttrs(self.payload["tokenAttrs"])
        self.profile = Profile(self.payload["profile"])

    def process(self, custom_data: dict):
        print(self.tokenAttrs.token)
        custom_data["return_method"](self.tokenAttrs.token)