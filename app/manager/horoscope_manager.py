"""
Author: nikhil.anand
Created at: 19/07/25
"""

from bs4 import BeautifulSoup
from requests import Response

from app.client.http_client import HttpClient
from app.constants.enum import ZodiacSignEnum
from app.constants.zodiac_sign_to_number_map import ZODIAC_SIGN_TO_NUMBER_MAP


class HoroscopeManager:
    """
    Manager class for fetching daily horoscopes from external sources.

    This class handles the retrieval of daily horoscope content for different
    zodiac signs by scraping horoscope websites and extracting the relevant text.

    Attributes:
        http_client (HttpClient): HTTP client for making web requests
        HOROSCOPE_WEBSITE_URL (str): Template URL for horoscope website
    """

    def __init__(self) -> None:
        """
        Initialize the HoroscopeManager with HTTP client and website URL.

        Sets up the HTTP client for web scraping and defines the base URL
        template for fetching horoscope content.
        """
        self.http_client = HttpClient()
        self.HOROSCOPE_WEBSITE_URL = (
            "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={}"
        )

    def get_horoscope(self, zodiac_sign: ZodiacSignEnum) -> str:
        """
        Fetch the daily horoscope for a specific zodiac sign.

        This method retrieves the daily horoscope content by making an HTTP request
        to the horoscope website, parsing the HTML response, and extracting the
        horoscope text from the main content area.

        Args:
            zodiac_sign (ZodiacSignEnum): The zodiac sign for which to fetch the horoscope

        Returns:
            str: The daily horoscope text for the specified zodiac sign

        Raises:
            requests.exceptions.RequestException: If the HTTP request fails
            AttributeError: If the expected HTML structure is not found
            KeyError: If the zodiac sign is not found in the mapping

        Example:
            >>> manager = HoroscopeManager()
            >>> horoscope = manager.get_horoscope(ZodiacSignEnum.ARIES)
            >>> print(horoscope)
            "Today brings new opportunities for Aries..."
        """
        webpage: Response = self.http_client.get(
            self.HOROSCOPE_WEBSITE_URL.format(ZODIAC_SIGN_TO_NUMBER_MAP[zodiac_sign])
        )
        soup = BeautifulSoup(webpage.content, "html.parser")
        data = soup.find("div", attrs={"class": "main-horoscope"})
        horoscope: str = data.p.text
        return horoscope
