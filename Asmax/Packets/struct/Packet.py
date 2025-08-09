import json

import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader


class Packet:
    def __init__(self, header: PacketHeader):
        self.header = header

    def send(self, payload: dict, ws: websocket.WebSocket):
        packet_json = {
            "ver": self.header.ver,
            "cmd": self.header.cmd,
            "seq": self.header.seq,
            "opcode": self.header.opcode,
            "payload": payload
        }
        ws.send(json.dumps(packet_json))