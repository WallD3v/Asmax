import json
import logging
from typing import Optional

import websocket

from Asmax.Packets.struct.AnswerPacket import AnswerPacket
from Asmax.Packets.struct.PacketHeader import PacketHeader
from Asmax.Packets.struct.RegisteredPacket import RegisteredPacket


class MaxConnection:
    def __init__(self, ws: websocket.WebSocket):
        self.registered_classes: list[RegisteredPacket] = []
        self.packet_query: list[AnswerPacket] = []
        self.conn = ws

    def register_packet(self, header: PacketHeader, clazz: type, custom_data: dict = {}):
        r_packet = RegisteredPacket(header, clazz, custom_data)
        self.registered_classes.append(r_packet)

    def process(self):
        while True:
            if not self.conn.connected:
                break
            packets = self.packet_query.copy()
            for packet in packets:
                packet_ = None
                for r_packet in self.registered_classes:
                    if packet.header.ver == r_packet.header.ver:
                        if packet.header.seq == r_packet.header.seq or r_packet.header.seq == -1:
                            if packet.header.cmd == r_packet.header.cmd:
                                if packet.header.opcode == r_packet.header.opcode:
                                    packet_ = r_packet
                if packet_ is None:
                    if packet.header.cmd == 3:
                        logging.error(packet.payload['localizedMessage'] + " " + packet.payload['message'])
                    else:
                        logging.warning(f"Unknown packet!\nHeader {packet.header.ver} {packet.header.cmd} {packet.header.seq} {packet.header.opcode}\nPayload {packet.payload}")
                else:
                    packet.payload["__conn"] = self.conn
                    parsed_packet = packet_.clazz(packet.header, packet.payload)
                    packet_.custom_data["__conn"] = self.conn
                    parsed_packet.process(packet_.custom_data)
                self.packet_query.remove(packet)

    def receive_packet(self) -> Optional[AnswerPacket]:
        try:
            packet_raw = self.conn.recv()
            packet_json = json.loads(packet_raw)
            packet = AnswerPacket(
                PacketHeader(
                    packet_json['ver'],
                    packet_json['cmd'],
                    packet_json['seq'],
                    packet_json['opcode']
                ),
                packet_json['payload']
            )
            return packet
        except websocket._exceptions.WebSocketConnectionClosedException:
            logging.warning("Connection lost.")
            return None

    def receive_packets(self):
        while True:
            packet = self.receive_packet()
            if packet is None:
                break
            self.packet_query.append(packet)