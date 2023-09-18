class HpMessageParser:
     
    _message_counter: dict[str, int] = dict()
    _message_counter_callbacks: dict[str, list] = dict()

    @classmethod
    def put_in_queue(cls, data: bytes, id: str):
        pass

    @classmethod
    def subscribe_message_counter(cls, id: str, func):
        if not id in cls._message_counter_callbacks:
            cls._message_counter_callbacks[id] = [func,]
        else:
            cls._message_counter_callbacks[id].append(func)

    @classmethod
    def unsubscribe_message_counter(cls, id: str, func):
        if id not in cls._message_counter_callbacks:
            return
        if func in cls._message_counter_callbacks[id]:
            cls._message_counter_callbacks[id].remove(func)
        if len(cls._message_counter_callbacks[id]) == 0:
            del cls._message_counter_callbacks[id]

    @classmethod
    def _trigger_message_counter(cls, id: str):
        value = cls._message_counter[id]
        for func in cls._message_counter_callbacks[id]:
            func(value)