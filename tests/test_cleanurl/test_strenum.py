from enum import IntEnum

from cleanurl import strenum


class TestStrEnum:

    class _TestEnum(strenum.StrEnum):
        VALUE_1 = 'value_1'
        VALUE_2 = 'value_2'

    def test_str_values(self):
        assert tuple(self._TestEnum.values()) == tuple(
            field.value  # type: ignore
            for field in self._TestEnum
        )

    def test_to_str(self):
        assert str(self._TestEnum.VALUE_1) == self._TestEnum.VALUE_1.value


class TestEnum2Str:

    class _TestStrEnum(str, strenum.Enum2Str):
        VALUE_1 = 'value_1'
        VALUE_2 = 'value_2'

    class _TestIntEnum(IntEnum, strenum.Enum2Str):
        VALUE_1 = 1
        VALUE_2 = 2

    def test_strenum2_str(self):
        assert str(self._TestStrEnum.VALUE_1) == self._TestStrEnum.VALUE_1.value

    def test_intenum2_str(self):
        assert str(self._TestIntEnum.VALUE_1) == str(self._TestIntEnum.VALUE_1.value)
