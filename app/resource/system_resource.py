"""
Author: nikhil.anand
Created at: 19/07/25
"""

from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.head("/v1")
def health_check_head() -> Dict[str, str]:
    """
    Health check endpoint using HEAD method.

    This endpoint provides a lightweight health check for the Astro Insights service
    using the HEAD HTTP method. It returns basic service status information.

    Returns:
        Dict[str, str]: A dictionary containing:
            - message (str): Service status message
            - author (str): Service author information

    Example:
        Response:
        {
            "message": "Astro Insights Service is running",
            "author": "nikhil.anand"
        }
    """
    return {"message": "Astro Insights Service is running", "author": "nikhil.anand"}


@router.get("/v1")
def health_check_get() -> Dict[str, str]:
    """
    Health check endpoint using GET method.

    This endpoint provides a health check for the Astro Insights service using
    the GET HTTP method. It returns basic service status information and can be
    used for monitoring and load balancer health checks.

    Returns:
        Dict[str, str]: A dictionary containing:
            - message (str): Service status message
            - author (str): Service author information

    Example:
        Response:
        {
            "message": "Astro Insights Service is running",
            "author": "nikhil.anand"
        }
    """
    return {"message": "Astro Insights Service is running", "author": "nikhil.anand"}
