import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class SendMessagePacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 17, 64))
        self.ws = ws

    def send_packet(self, chat_id: int, text: str, notify: bool):
        payload = {
            "chatId": chat_id,
            "message": {
                "text": text,
                "cid": MaxUtils.get_timestamp(),
                "elements": [],
                "attaches": []

            },
            "notify": notify
        }
        self.send(payload, self.ws)

class SendReplyMessagePacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 17, 64))
        self.ws = ws

    def send_packet(self, chat_id: int, text: str, messageId: str, notify: bool):
        payload = {
          "chatId": chat_id,
          "message": {
            "text": text,
            "cid": MaxUtils.get_timestamp(),
            "elements": [],
            "link": {
              "type": "REPLY",
              "messageId": messageId
            },
            "attaches": []
          },
          "notify": notify
        }
        self.send(payload, self.ws)

class SendStickerPacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 17, 64))
        self.ws = ws

    def send_packet(self, chat_id: int, sticker_id: int, notify: bool):
        payload = {
          "chatId": chat_id,
          "message": {
            "cid": MaxUtils.get_timestamp(),
            "attaches": [
              {
                "_type": "STICKER",
                "stickerId": sticker_id
              }
            ]
          },
          "notify": notify
        }
        self.send(payload, self.ws)

class SendReplyStickerPacket(Packet):
    def __init__(self, ws: websocket.WebSocket):
        super().__init__(PacketHeader(11, 0, 17, 64))
        self.ws = ws

    def send_packet(self, chat_id: int, sticker_id: int, reply_messageId: str, notify: bool):
        payload = {
          "chatId": chat_id,
          "message": {
            "cid": MaxUtils.get_timestamp(),
            "link": {
              "type": "REPLY",
              "messageId": reply_messageId
            },
            "attaches": [
              {
                "_type": "STICKER",
                "stickerId": sticker_id
              }
            ]
          },
          "notify": notify
        }
        self.send(payload, self.ws)