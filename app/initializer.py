"""
Author: nikhil.anand
Created at: 19/07/25
"""

from fastapi import FastAPI
from fastapi.logger import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.resource import insight_resource, system_resource
from app.cache.horoscope_cache import HoroscopeCache

scheduler = AsyncIOScheduler()


def init(app: FastAPI) -> None:
    """
    Initialize the FastAPI application with routers and scheduled tasks.

    This function sets up the complete application initialization including
    API routers and background scheduled tasks for cache management.

    Args:
        app (FastAPI): The FastAPI application instance to initialize
    """
    init_routers(app)
    init_scheduled_tasks(app)


def init_routers(app: FastAPI) -> None:
    """
    Initialize and register API routers with the FastAPI application.

    This function registers all the API route handlers including system
    health check endpoints and insight generation endpoints.

    Args:
        app (FastAPI): The FastAPI application instance to register routers with

    Registered Routers:
        - system_resource.router: Health check and system status endpoints
        - insight_resource.router: Astrological insight generation endpoints
    """
    logger.info(msg="Initializing routers")
    app.include_router(system_resource.router)
    app.include_router(insight_resource.router)


def init_scheduled_tasks(app: FastAPI) -> None:
    """
    Initialize scheduled background tasks for the application.

    This function sets up the AsyncIO scheduler with cron jobs for periodic
    maintenance tasks such as cache cleanup. It registers startup and shutdown
    event handlers for proper scheduler lifecycle management.

    Args:
        app (FastAPI): The FastAPI application instance to register event handlers with

    Scheduled Tasks:
        - Cache cleanup: Runs daily at midnight to remove stale horoscope cache entries
    """

    @app.on_event("startup")
    async def start_scheduler() -> None:
        """
        Start the background scheduler on application startup.

        This event handler initializes the AsyncIO scheduler and adds the
        cache cleanup job to run daily at midnight.
        """
        scheduler.add_job(clear_stale_horoscope_cache, CronTrigger(hour=0, minute=0, second=0), id="clear_stale_cache")
        scheduler.start()
        logger.info("Scheduler started - stale cache cleanup at midnight")

    @app.on_event("shutdown")
    async def shutdown_scheduler() -> None:
        """
        Shutdown the background scheduler on application shutdown.

        This event handler ensures proper cleanup of the scheduler when
        the application is shutting down.
        """
        scheduler.shutdown()
        logger.info("Scheduler shutdown")


def clear_stale_horoscope_cache() -> None:
    """
    Clear stale horoscope cache entries.

    This function is executed as a scheduled task to remove outdated
    horoscope cache entries that are no longer valid (not from today).
    It helps maintain cache efficiency and prevents memory bloat.

    The function logs the number of entries removed for monitoring purposes.
    """
    logger.info("Clearing stale horoscope cache entries")
    cache = HoroscopeCache()
    removed_count: int = cache.clear_stale_entries()
    logger.info(f"Cleared {removed_count} stale horoscope cache entries")
