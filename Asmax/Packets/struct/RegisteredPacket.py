from Asmax.Packets.struct.PacketHeader import PacketHeader


class RegisteredPacket:
    def __init__(self, header: PacketHeader, clazz: type, custom_data: dict):
        self.header = header
        self.clazz = clazz
        self.custom_data = custom_data