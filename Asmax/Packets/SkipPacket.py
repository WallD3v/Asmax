import websocket

from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.Packet import Packet
from Asmax.Utils.MaxUtils import MaxUtils

class SkipPacket(AnswerPacket):
    def __init__(self, header: PacketHeader, payload: dict):
        super().__init__(header, payload)

    def process(self, custom_data: dict):
        pass