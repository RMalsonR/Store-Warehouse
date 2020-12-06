from enum import Enum


class Status(Enum):
    NEW = 'NEW'
    IN_PROCESS = 'IN_PROCESS'
    STORED = 'STORED'
    SEND = 'SEND'

    @classmethod
    def as_choices(cls):
        return (
            (cls.NEW.value, 'New order'),
            (cls.IN_PROCESS.value, 'Order in process'),
            (cls.STORED.value, 'Order stored'),
            (cls.SEND.value, 'Order sent')
        )
