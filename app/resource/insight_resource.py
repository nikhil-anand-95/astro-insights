"""
Author: nikhil.anand
Created at: 19/07/25
"""

import traceback

from fastapi import APIRouter
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from app.dto.request.insight_request import InsightRequest
from app.manager.insight_manager import InsightManager

router = APIRouter()

insight_manager = InsightManager()


@router.post("/v1/generate-insight")
def generate_insight(request: InsightRequest) -> JSONResponse:
    """
    Generate personalized astrological insight based on user's birth information.

    This endpoint processes a user's birth details to generate a personalized horoscope
    insight. It determines the zodiac sign, fetches the daily horoscope, and personalizes
    it using AI models. The response can be in English or Hindi based on the request.

    Args:
        request (InsightRequest): The insight request containing:
            - name (str): User's name for personalization
            - birth_date (str): Birth date in parseable format (e.g., "1995-01-15")
            - birth_time (str): Birth time (currently not used in processing)
            - birth_place (str): Birth place (currently not used in processing)
            - language (ResponseLanguageEnum, optional): Response language (English/Hindi)

    Returns:
        JSONResponse: A JSON response containing:
            - On success (200): InsightResponse with zodiac sign, personalized insight, and language
            - On error (500): Error message with details

    Raises:
        ValueError: When birth_date format is invalid
        Exception: For any other processing errors

    Example:
        Request:
        {
            "name": "John",
            "birth_date": "1995-01-15",
            "birth_time": "10:30",
            "birth_place": "New York",
            "language": "ENGLISH"
        }

        Response:
        {
            "zodiac": "CAPRICORN",
            "insight": "Hello John, today brings...",
            "language": "ENGLISH"
        }
    """
    try:
        logger.info(msg=f"Received insight generation request for user {request.name}")
        insight_response = insight_manager.generate_astrological_insight(request)
        return JSONResponse(content=insight_response.model_dump(), status_code=200)
    except Exception as e:
        error_message = "Error in generating astrological insight due to {}".format(e)
        logger.error(msg=error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)
