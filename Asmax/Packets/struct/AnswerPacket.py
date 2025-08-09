import json

from Asmax.Packets.struct.PacketHeader import PacketHeader


class AnswerPacket:
    def __init__(self, header: PacketHeader, payload: dict):
        self.header = header
        self.payload = payload

    @staticmethod
    def parse(packet_raw: str) -> 'AnswerPacket':
        data = json.loads(packet_raw)
        packet = AnswerPacket(
            PacketHeader(
                data["ver"],
                data["cmd"],
                data["seq"],
                data["opcode"]
            ),
            data["payload"]
        )
        return packet