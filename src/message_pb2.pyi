from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MsgDeliveryRequest(_message.Message):
    __slots__ = ["id", "interface", "money", "clock"]
    ID_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    id: int
    interface: str
    money: int
    clock: int
    def __init__(self, id: _Optional[int] = ..., interface: _Optional[str] = ..., money: _Optional[int] = ..., clock: _Optional[int] = ...) -> None: ...

class MsgDeliveryReply(_message.Message):
    __slots__ = ["interface", "result", "money", "clock"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    money: int
    clock: int
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., money: _Optional[int] = ..., clock: _Optional[int] = ...) -> None: ...
