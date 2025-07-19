"""
Author: nikhil.anand
Created at: 19/07/25
"""

from typing import Optional

from pydantic import BaseModel, Field

from app.constants.enum import ResponseLanguageEnum


class InsightRequest(BaseModel):
    """
    Request model for astrological insight generation.

    This Pydantic model defines the structure and validation rules for
    requests to generate personalized astrological insights. It contains
    all the necessary user information required for horoscope personalization.

    Attributes:
        name (str): User's name for personalization
        birth_date (str): Birth date in parseable format (e.g., "1995-01-15", "15/01/1995")
        birth_time (str): Birth time (currently not used in processing but collected for future features)
        birth_place (str): Birth place (currently not used in processing but collected for future features)
        language (Optional[ResponseLanguageEnum]): Preferred response language, defaults to English

    Example:
        >>> request = InsightRequest(
        ...     name="John Doe",
        ...     birth_date="1995-01-15",
        ...     birth_time="10:30 AM",
        ...     birth_place="New York, NY",
        ...     language=ResponseLanguageEnum.ENGLISH,
        ... )
        >>> print(request.name)
        "John Doe"
    """

    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    language: Optional[ResponseLanguageEnum] = Field(default=ResponseLanguageEnum.ENGLISH)
