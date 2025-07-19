"""
Astro Insights Service - Main Application Module

Author: nikhil.anand
Created at: 19/07/25

This module serves as the entry point for the Astro Insights FastAPI application.
It initializes the FastAPI app with proper configuration and sets up all
necessary components including routers, scheduled tasks, and middleware.
"""

from fastapi import FastAPI
from fastapi.logger import logger

from app.initializer import init

logger.info(msg="Starting Astro Insights Service v0.0.1!!!")

app: FastAPI = FastAPI(
    title="Astro Insights",
    description="""
    Astro Insights Service - Personalized Astrological Insights API
    
    This service provides personalized astrological insights based on user's birth information.
    It combines zodiac sign determination, daily horoscope fetching, and AI-powered personalization
    to deliver customized horoscope content in multiple languages.
    
    ## Features
    
    * **Zodiac Sign Detection**: Automatically determines zodiac sign from birth date
    * **Daily Horoscope Fetching**: Retrieves fresh horoscope content from external sources
    * **AI Personalization**: Uses advanced language models (TinyLlama, GPT-2) for personalization
    * **Multi-language Support**: Supports English and Hindi responses
    * **Intelligent Caching**: Caches personalized horoscopes for improved performance
    * **Health Monitoring**: Provides health check endpoints for monitoring
    
    ## API Endpoints
    
    * `GET/HEAD /v1` - Health check endpoints
    * `POST /v1/generate-insight` - Generate personalized astrological insight
    
    ## Supported Languages
    
    * English (default)
    * Hindi (via Helsinki-NLP translation)
    """,
    version="0.0.1",
    contact={
        "name": "Nikhil Anand",
        "email": "nikhilanand01.95@gmail.com",
    },
    debug=True,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Initialize the application with routers and scheduled tasks
init(app)
