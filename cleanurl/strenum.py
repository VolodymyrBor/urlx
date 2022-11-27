from enum import Enum
from typing import Iterable


class StrEnum(str, Enum):

    @classmethod
    def str_values(cls) -> Iterable[str]:
        for item in cls:
            yield item.value  # type: ignore

    def __str__(self) -> str:
        return self.value  # type: ignore
