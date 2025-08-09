import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class PreparePacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 0, 6))
        self.ws = ws

    def send_packet(self, device_type: str, locale: str, device_locale: str, os_version: str, device_name: str, header_user_agent: str, app_version: str, screen: str, timezone: str):
        payload = {
            "userAgent": {
                "deviceType": device_type,
                "locale": locale,
                "deviceLocale": device_locale,
                "osVersion": os_version,
                "deviceName": device_name,
                "headerUserAgent": header_user_agent,
                "appVersion": app_version,
                "screen": screen,
                "timezone": timezone
            },
            "deviceId": f"{MaxUtils.random_str(12)}"
        }
        self.send(payload, self.ws)

class PrepareAnswerPacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        super().__init__(header, payload)
        self.location = self.payload["location"]
        self.app_update_type = self.payload["app-update-type"]

    def process(self, custom_data: dict):
        pass