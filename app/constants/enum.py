"""
Author: nikhil.anand
Created at: 19/07/25
"""

from enum import Enum


class ZodiacSignEnum(Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"


class ResponseLanguageEnum(Enum):
    ENGLISH = "en"
    HINDI = "hi"


class LlmModelsEnum(Enum):
    TINY_LLAMA = "TINY_LLAMA"
    GPT2 = "GPT2"


class TranslatorModelsEnum(Enum):
    HELSINKI = "HELSINKI"
