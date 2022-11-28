from enum import IntEnum

from cleanurl import strenum


class TestStrEnum:

    class TestEnum(strenum.StrEnum):
        VALUE_1 = 'value_1'
        VALUE_2 = 'value_2'

    def test_str_values(self):
        assert tuple(self.TestEnum.values()) == tuple(
            field.value  # type: ignore
            for field in self.TestEnum
        )

    def test_to_str(self):
        assert str(self.TestEnum.VALUE_1) == self.TestEnum.VALUE_1.value


class TestEnum2Str:

    class TestStrEnum(str, strenum.Enum2Str):
        VALUE_1 = 'value_1'
        VALUE_2 = 'value_2'

    class TestIntEnum(IntEnum, strenum.Enum2Str):
        VALUE_1 = 1
        VALUE_2 = 2

    def test_strenum2_str(self):
        assert str(self.TestStrEnum.VALUE_1) == self.TestStrEnum.VALUE_1.value

    def test_intenum2_str(self):
        assert str(self.TestIntEnum.VALUE_1) == str(self.TestIntEnum.VALUE_1.value)
