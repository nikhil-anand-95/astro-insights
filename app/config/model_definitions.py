"""
Author: nikhil.anand
Created at: 20/07/25
"""

from app.config.model_config import ModelConfig, TranslatorConfig
from app.constants.enum import LlmModelsEnum, TranslatorModelsEnum
from app.constants.llm_constants import GPT2_MODEL_PERSONALIZATION_PROMPT, TINY_LLAMA_MODEL_PERSONALIZATION_PROMPT

# Model Configurations
MODEL_CONFIGURATIONS = {
    LlmModelsEnum.TINY_LLAMA: ModelConfig(
        model_type=LlmModelsEnum.TINY_LLAMA,
        enabled=True,
        prompt=TINY_LLAMA_MODEL_PERSONALIZATION_PROMPT,
        description="Optimized for chat/instruction following with modern architecture",
    ),
    LlmModelsEnum.GPT2: ModelConfig(
        model_type=LlmModelsEnum.GPT2,
        enabled=False,
        prompt=GPT2_MODEL_PERSONALIZATION_PROMPT,
        description="General purpose text generation model with legacy architecture",
    ),
}

# Translator Configurations
TRANSLATOR_CONFIGURATIONS = {
    TranslatorModelsEnum.HELSINKI: TranslatorConfig(
        translator_type=TranslatorModelsEnum.HELSINKI,
        enabled=True,
        description="Helsinki-NLP English to Hindi translator with good compatibility",
        supported_languages=["hi"],
    ),
}
