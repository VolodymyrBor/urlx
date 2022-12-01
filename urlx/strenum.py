from enum import Enum
from typing import Iterable


class Enum2Str(Enum):
    def __str__(self) -> str:
        return str(self.value)  # type: ignore


class StrEnum(str, Enum2Str):

    @classmethod
    def values(cls) -> Iterable[str]:
        for item in cls:
            yield item.value  # type: ignore
