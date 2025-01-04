import re
from typing import Union


class StringUtils:
    @staticmethod
    def to_snake_case(text: str) -> str:
        """Converts a given string from camel case or Pascal case to snake case.

        Args:
            text (str): The input string in camel case or Pascal case.

        Returns:
            str: The converted string in snake case.
        """
        pattern = re.compile(r"(?<!^)(?=[A-Z])")
        return pattern.sub("_", text).lower()

    @staticmethod
    def to_camel_case(text: str) -> str:
        """Converts a string from snake_case to camelCase.

        Args:
            text (str): The input string in snake_case format.

        Returns:
            str: The converted string in camelCase format.
        """
        components = text.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def to_title_case(text: str) -> str:
        """Converts a given string to title case.

        Title case means that the first letter of each word is capitalized, while the rest of the letters are in lowercase.

        Args:
            text (str): The input string to be converted to title case.

        Returns:
            str: The input string converted to title case.
        """
        return " ".join(word.capitalize() for word in text.split())

    @staticmethod
    def remove_special_chars(text: str, keep_chars: str = "") -> str:
        """Removes special characters from a given text string, optionally allowing certain characters to be retained.

        Args:
            text (str): The input string from which special characters will be removed.
            keep_chars (str, optional): A string of characters that should not be removed from the input text. Defaults to an empty string.

        Returns:
            str: A new string with special characters removed, retaining any specified characters.
        """
        pattern = f"[^a-zA-Z0-9{keep_chars}]"
        return re.sub(pattern, "", text)

    @staticmethod
    def truncate(text: str, length: int, suffix: str = "...") -> str:
        """Truncate a string to a specified length and append a suffix if truncated.

        Args:
            text (str): The string to be truncated.
            length (int): The maximum length of the returned string, including the suffix.
            suffix (str, optional): The suffix to append if the string is truncated. Defaults to "...".

        Returns:
            str: The truncated string with the suffix if the original string exceeds the specified length; otherwise, the original string.
        """
        if len(text) <= length:
            return text
        return text[: length - len(suffix)] + suffix

    @staticmethod
    def format_number(number: Union[int, float], decimals: int = 2) -> str:
        """Formats a number as a string with commas as thousands separators and a specified number of decimal places.

        Args:
            number (Union[int, float]): The number to format. Can be an integer or a float.
            decimals (int, optional): The number of decimal places to include if the number is a float. Defaults to 2.

        Returns:
            str: The formatted number as a string.
        """
        if isinstance(number, int):
            return f"{number:,}"
        return f"{number:,.{decimals}f}"

    @staticmethod
    def mask_string(
        text: str, mask_char: str = "*", expose_left: int = 0, expose_right: int = 0
    ) -> str:
        """Masks a string by replacing a portion of it with a specified character.

        Args:
            text (str): The input string to be masked.
            mask_char (str, optional): The character to use for masking. Defaults to '*'.
            expose_left (int, optional): The number of characters to expose from the left. Defaults to 0.
            expose_right (int, optional): The number of characters to expose from the right. Defaults to 0.

        Returns:
            str: The masked string with specified characters exposed on both ends.

        Raises:
            ValueError: If `mask_char` is an empty string.

        Examples:
            >>> mask_string("HelloWorld", "*", 3, 2)
            'Hel******ld'

            >>> mask_string("Secret", "#", 2, 1)
            'Se###t'

            >>> mask_string("Short", "*", 5, 0)
            'Short'
        """
        if len(text) <= expose_left + expose_right:
            return text
        return (
            text[:expose_left]
            + mask_char * (len(text) - expose_left - expose_right)
            + text[-expose_right:]
        )

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Checks if the provided email address is valid based on a regular expression pattern.

        Args:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email address is valid, False otherwise.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
