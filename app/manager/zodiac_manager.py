"""
Author: nikhil.anand
Created at: 19/07/25
"""

from datetime import date

from zodiac_sign import get_zodiac_sign

from app.constants.enum import ZodiacSignEnum


class ZodiacManager:
    """
    Manager class for determining zodiac signs based on birth dates.

    This class provides functionality to calculate a person's zodiac sign
    based on their birth date using the zodiac_sign library and converts
    the result to the application's ZodiacSignEnum format.

    Note:
        This class uses the external 'zodiac_sign' library for accurate
        zodiac sign calculation based on astronomical data.
    """

    def __init__(self) -> None:
        """
        Initialize the ZodiacManager.

        Currently, no initialization is required as the class uses
        static methods and external library functions.
        """
        pass

    @staticmethod
    def get_zodiac_sign(birth_date: date) -> ZodiacSignEnum:
        """
        Determine the zodiac sign for a given birth date.

        This method calculates the zodiac sign based on the provided birth date
        using the zodiac_sign library and converts the result to the application's
        ZodiacSignEnum format for consistent usage throughout the system.

        Args:
            birth_date (date): The birth date for which to determine the zodiac sign

        Returns:
            ZodiacSignEnum: The zodiac sign corresponding to the birth date

        Raises:
            KeyError: If the zodiac sign returned by the library is not found
                     in the ZodiacSignEnum
            ValueError: If the birth_date is invalid or cannot be processed
        """
        zodiac_sign: str = get_zodiac_sign(birth_date)
        return ZodiacSignEnum[zodiac_sign.upper()]
