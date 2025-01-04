import pytest
from datetime import datetime
from core.utils.dateutils import DateUtils


class TestDateUtils:
    def test_parse_date(self) -> None:
        date_str = "2024-12-24"
        result = DateUtils.parse_date(date_str)
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 12
        assert result.day == 24

    def test_parse_date_custom_format(self) -> None:
        date_str = "24/12/2024"
        result = DateUtils.parse_date(date_str, "%d/%m/%Y")
        assert result.day == 24
        assert result.month == 12
        assert result.year == 2024

    def test_format_date(self) -> None:
        date_str = "24/12/2024"
        result = DateUtils.format_date(date_str, "%d/%m/%Y")
        assert result == "24/12/2024"

    def test_format_date_with_datetime(self) -> None:
        date = datetime(2024, 12, 24)
        result = DateUtils.format_date(date, "%Y-%m-%d")
        assert result == "2024-12-24"

    @pytest.mark.parametrize(
        "unit,expected",  # type: ignore
        [("days", 1), ("hours", 24), ("minutes", 1440), ("seconds", 86400)],
    )
    def test_get_date_diff_units(self, unit: str, expected: int) -> None:
        date1 = "2024-12-24"
        date2 = "2024-12-25"
        result = DateUtils.get_date_diff(date1, date2, unit)
        assert result == expected

    def test_get_date_diff_negative(self) -> None:
        date1 = "2024-12-25"
        date2 = "2024-12-24"
        result = DateUtils.get_date_diff(date1, date2, "days")
        assert result == -1

    @pytest.mark.parametrize(
        "unit,value,expected",  # type: ignore
        [
            ("days", 2, "2024-12-26"),
            ("hours", 48, "2024-12-26"),
            ("minutes", 2880, "2024-12-26"),
            ("seconds", 172800, "2024-12-26"),
        ],
    )
    def test_add_time(self, unit, value, expected) -> None:
        date = "2024-12-24"
        result = DateUtils.add_time(date, value, unit)
        assert DateUtils.format_date(result) == expected

    def test_invalid_format_raises_error(self) -> None:
        with pytest.raises(ValueError):
            DateUtils.parse_date("2024-13-45")
