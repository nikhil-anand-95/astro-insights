"""
Author: nikhil.anand
Created at: 20/07/25
"""

from dataclasses import dataclass

from app.constants.enum import LlmModelsEnum, TranslatorModelsEnum


@dataclass
class ModelConfig:
    """
    Configuration class for LLM models.

    Attributes:
        model_type (LlmModelsEnum): The type of the model
        enabled (bool): Whether the model is enabled for use
        prompt (str): The personalization prompt for the model
        description (str): Human-readable description of the model
    """

    model_type: LlmModelsEnum
    enabled: bool
    prompt: str
    description: str


@dataclass
class TranslatorConfig:
    """
    Configuration class for translator models.

    Attributes:
        translator_type (TranslatorModelsEnum): The type of the translator
        enabled (bool): Whether the translator is enabled for use
        description (str): Human-readable description of the translator
        supported_languages (list[str]): List of supported language codes
    """

    translator_type: TranslatorModelsEnum
    enabled: bool
    description: str
    supported_languages: list[str]
