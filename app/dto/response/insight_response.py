"""
Author: nikhil.anand
Created at: 19/07/25
"""

from pydantic import BaseModel, Field

from app.constants.enum import ResponseLanguageEnum, ZodiacSignEnum


class InsightResponse(BaseModel):
    """
    Response model for astrological insight generation.

    This Pydantic model defines the structure of the response returned
    after generating a personalized astrological insight. It contains
    the user's zodiac sign, personalized insight text, and language information.

    Attributes:
        zodiac (ZodiacSignEnum): The user's zodiac sign based on their birth date
        insight (str): Personalized horoscope text tailored for the user
        language (ResponseLanguageEnum): The language of the insight response
    """

    zodiac: ZodiacSignEnum
    insight: str
    language: ResponseLanguageEnum

    class Config:
        """
        Pydantic model configuration.

        Configuration settings for the InsightResponse model to control
        serialization behavior and enum handling.

        Attributes:
            use_enum_values (bool): Use enum values instead of enum names in serialization
        """

        use_enum_values = True
