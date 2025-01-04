import pytest
from typing import Union

from core.utils.stringutils import StringUtils


class TestStringUtils:
    @pytest.mark.parametrize(
        "input_str,expected",  # type: ignore
        [
            ("helloWorld", "hello_world"),
            ("HelloWorld", "hello_world"),
            ("hello_world", "hello_world"),
            ("ABC", "a_b_c"),
        ],
    )
    def test_to_snake_case(self, input_str: str, expected: str) -> None:
        assert StringUtils.to_snake_case(input_str) == expected

    @pytest.mark.parametrize(
        "input_str,expected",  # type: ignore
        [
            ("hello_world", "helloWorld"),
            ("hello", "hello"),
            ("hello_world_test", "helloWorldTest"),
        ],
    )
    def test_to_camel_case(self, input_str: str, expected: str) -> None:
        assert StringUtils.to_camel_case(input_str) == expected

    @pytest.mark.parametrize(
        "input_str,expected",  # type: ignore
        [
            ("hello world", "Hello World"),
            ("HELLO WORLD", "Hello World"),
            ("hello", "Hello"),
        ],
    )
    def test_to_title_case(self, input_str: str, expected: str) -> None:
        assert StringUtils.to_title_case(input_str) == expected

    @pytest.mark.parametrize(
        "input_str,keep_chars,expected",  # type: ignore
        [
            ("hello@world!", "", "helloworld"),
            ("hello@world!", "@", "hello@world"),
            ("test123!@#", "", "test123"),
        ],
    )
    def test_remove_special_chars(
        self, input_str: str, keep_chars: str, expected: str
    ) -> None:
        assert StringUtils.remove_special_chars(input_str, keep_chars) == expected

    @pytest.mark.parametrize(
        "input_str,length,suffix,expected",  # type: ignore
        [
            ("hello world", 5, "...", "he..."),
            ("hello", 10, "...", "hello"),
            ("hello world", 8, "..", "hello .."),
        ],
    )
    def test_truncate(
        self, input_str: str, length: int, suffix: str, expected: str
    ) -> None:
        assert StringUtils.truncate(input_str, length, suffix) == expected

    @pytest.mark.parametrize(
        "number,decimals,expected",  # type: ignore
        [
            (1234567, 2, "1,234,567"),
            (1234.5678, 2, "1,234.57"),
            (1234.5678, 3, "1,234.568"),
        ],
    )
    def test_format_number(
        self, number: Union[int, float], decimals: int, expected: str
    ) -> None:
        assert StringUtils.format_number(number, decimals) == expected

    @pytest.mark.parametrize(
        "input_str,mask_char,expose_left,expose_right,expected",  # type: ignore
        [
            ("1234567890", "*", 4, 2, "1234****90"),
            ("password", "*", 2, 2, "pa****rd"),
            ("short", "*", 2, 2, "sh*rt"),
        ],
    )
    def test_mask_string(
        self,
        input_str: str,
        mask_char: str,
        expose_left: int,
        expose_right: int,
        expected: str,
    ) -> None:
        assert (
            StringUtils.mask_string(input_str, mask_char, expose_left, expose_right)
            == expected
        )

    @pytest.mark.parametrize(
        "email,expected",  # type: ignore
        [
            ("test@example.com", True),
            ("invalid.email", False),
            ("test@test@test.com", False),
            ("test.name+label@example.co.uk", True),
        ],
    )
    def test_is_valid_email(self, email: str, expected: bool) -> None:
        assert StringUtils.is_valid_email(email) == expected
