from datetime import datetime, timedelta
from typing import Union, Callable
from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger

logger = AzureOpenTelemetryLogger().logger


class DateUtils:
    @staticmethod
    def parse_date(date_str: str, format: str = "%Y-%m-%d") -> datetime:
        """Parse a date string into a datetime object.

        Args:
            date_str (str): The date string to be parsed.
            format (str, optional): The format of the date string. Defaults to "%Y-%m-%d".

        Returns:
            datetime: A datetime object representing the parsed date.

        Raises:
            ValueError: If the date_str does not match the format.
        """
        return datetime.strptime(date_str, format)

    @staticmethod
    def format_date(date: Union[str, datetime], output_format: str = "%Y-%m-%d") -> str:
        """Formats a given date into a specified output format.

        Args:
            date (Union[str, datetime]): The date to format, which can be a string or a datetime object.
            output_format (str, optional): The format to output the date in. Defaults to "%Y-%m-%d".

        Returns:
            str: The formatted date as a string.
        """
        if isinstance(date, str):
            date = DateUtils.parse_date(date, output_format)
        return date.strftime(output_format)

    @staticmethod
    def get_date_diff(
        date1: Union[str, datetime], date2: Union[str, datetime], unit: str = "days"
    ) -> int:
        """Calculate the difference between two dates.

        Args:
            date1 (Union[str, datetime]): The first date, which can be a string or a datetime object.
            date2 (Union[str, datetime]): The second date, which can be a string or a datetime object.
            unit (str, optional): The unit of time for the difference. Can be "days", "hours", "minutes", or any other string. Defaults to "days".

        Returns:
            int: The difference between the two dates in the specified unit.

        Raises:
            ValueError: If the unit is not recognized.
        """
        if isinstance(date1, str):
            date1 = DateUtils.parse_date(date1)
        if isinstance(date2, str):
            date2 = DateUtils.parse_date(date2)

        diff = date2 - date1

        if unit == "days":
            return diff.days
        elif unit == "hours":
            return int(diff.total_seconds() / 3600)
        elif unit == "minutes":
            return int(diff.total_seconds() / 60)
        return int(diff.total_seconds())

    @staticmethod
    def add_time(
        date: Union[str, datetime], value: int, unit: str = "days"
    ) -> datetime:
        """Adds a specified amount of time to a given date.

        Args:
            date (Union[str, datetime]): The date to which time will be added.
                It can be a string in a recognized date format or a datetime object.
            value (int): The amount of time to add.
            unit (str, optional): The unit of time to add.
                Can be "days", "hours", "minutes", or "seconds". Defaults to "days".

        Returns:
            datetime: A new datetime object representing the date after the time has been added.

        Raises:
            ValueError: If the unit is not one of the recognized strings ("days", "hours", "minutes", "seconds").
        """
        if isinstance(date, str):
            date = DateUtils.parse_date(date)

        units: dict[str, Callable[[int], timedelta]] = {
            "days": lambda x: timedelta(days=x),
            "hours": lambda x: timedelta(hours=x),
            "minutes": lambda x: timedelta(minutes=x),
            "seconds": lambda x: timedelta(seconds=x),
        }
        if unit not in units:
            raise ValueError(
                f"Invalid unit '{unit}'. Valid units are 'days', 'hours', 'minutes', 'seconds'."
            )

        return date + units[unit](value)
