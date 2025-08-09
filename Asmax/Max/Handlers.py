from Asmax.Packets.ReceiveMessage import Message


class MaxHandlers:
    def __init__(self):
        self.message_handlers = []
        self.sticker_handlers = []

    def add_message_handler(self, handler):
        self.message_handlers.append(handler)

    async def process_message(self, message: Message):
        for handler in self.message_handlers:
            await handler(message)

    def add_sticker_handler(self, handler):
        self.sticker_handlers.append(handler)

    async def process_sticker(self, message: Message):
        for handler in self.sticker_handlers:
            await handler(message, message.attaches[0])