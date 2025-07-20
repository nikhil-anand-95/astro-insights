"""
Author: nikhil.anand
Created at: 19/07/25
"""

from datetime import date
from typing import Optional

from dateutil.parser import parse
from fastapi.logger import logger

from app.cache.horoscope_cache import HoroscopeCache
from app.constants.enum import ResponseLanguageEnum, ZodiacSignEnum
from app.dto.request.insight_request import InsightRequest
from app.dto.response.insight_response import InsightResponse
from app.manager.horoscope_manager import HoroscopeManager
from app.manager.llm_manager import LlmManager
from app.manager.zodiac_manager import ZodiacManager


class InsightManager:
    """
    Manager class for generating personalized astrological insights.

    This class orchestrates the process of generating personalized horoscope insights
    by coordinating zodiac sign determination, horoscope fetching, AI personalization,
    and caching mechanisms.

    Attributes:
        zodiac_manager (ZodiacManager): Handles zodiac sign determination
        horoscope_manager (HoroscopeManager): Fetches daily horoscopes
        llm_manager (LlmManager): Personalizes horoscopes using AI models
        cache (HoroscopeCache): Manages horoscope caching for performance
    """

    def __init__(self) -> None:
        """
        Initialize the InsightManager with required dependencies.

        Sets up managers for zodiac signs, horoscopes, LLM processing,
        and caching functionality.
        """
        self.zodiac_manager = ZodiacManager()
        self.horoscope_manager = HoroscopeManager()
        self.llm_manager = LlmManager()
        self.cache = HoroscopeCache()

    @staticmethod
    def _validate_date(date_str: str) -> Optional[date]:
        """
        Validate and parse a date string into a date object.

        Args:
            date_str (str): Date string in various formats (e.g., "1995-01-15", "15/01/1995")

        Returns:
            Optional[date]: Parsed date object if valid, None if invalid
        """
        try:
            date_obj = parse(date_str)
            return date_obj.date() if hasattr(date_obj, "date") else date_obj
        except Exception:
            logger.error(msg=f"Invalid date format for {date_str}")
            return None

    def generate_astrological_insight(self, request: InsightRequest) -> InsightResponse:
        """
        Generate a personalized astrological insight based on user's birth information.

        This method processes the user's birth date to determine their zodiac sign,
        fetches the daily horoscope, personalizes it using AI models, and handles
        caching for improved performance. The insight can be returned in English or Hindi.

        Args:
            request (InsightRequest): The insight request containing user's birth details
                and preferences including name, birth_date, and language preference

        Returns:
            InsightResponse: Personalized astrological insight containing:
                - zodiac (ZodiacSignEnum): User's zodiac sign
                - insight (str): Personalized horoscope text
                - language (ResponseLanguageEnum): Response language

        Raises:
            ValueError: If the birth_date format is invalid or cannot be parsed
        """
        dob: Optional[date] = self._validate_date(request.birth_date)
        if not dob:
            logger.error(msg=f"Error in generating insight for {request.name} due to date validation failure")
            raise ValueError(f"Error in generating insight due to Invalid date format")

        cached_horoscope = self.cache.get(
            birth_date=request.birth_date, name=request.name, language=request.language.value
        )

        if cached_horoscope:
            logger.info(f"Cache hit for {request.name}")
            zodiac_sign: ZodiacSignEnum = self.zodiac_manager.get_zodiac_sign(birth_date=dob)
            return InsightResponse(zodiac=zodiac_sign, insight=cached_horoscope, language=request.language)

        # Cache miss - generate new horoscope
        logger.info(f"Cache miss for {request.name}, generating new horoscope")
        zodiac_sign: ZodiacSignEnum = self.zodiac_manager.get_zodiac_sign(birth_date=dob)
        horoscope: str = self.horoscope_manager.get_horoscope(zodiac_sign=zodiac_sign)
        personalized_horoscope: str = self.llm_manager.personalize_horoscope(
            horoscope=horoscope, name=request.name, language=request.language
        )
        self.cache.put(
            birth_date=request.birth_date,
            name=request.name,
            horoscope=personalized_horoscope,
            language=request.language.value,
        )

        return InsightResponse(zodiac=zodiac_sign, insight=personalized_horoscope, language=request.language)
