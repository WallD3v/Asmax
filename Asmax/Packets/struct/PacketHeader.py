class PacketHeader:
    def __init__(self, ver: int, cmd: int, seq: int, opcode: int):
        self.ver = ver
        self.cmd = cmd
        self.seq = seq
        self.opcode = opcode