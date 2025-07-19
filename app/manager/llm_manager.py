"""
Author: nikhil.anand
Created at: 19/07/25
"""

from typing import Dict, Union

from app.constants.enum import LlmModelsEnum, ResponseLanguageEnum, TranslatorModelsEnum
from app.constants.llm_constants import GPT2_MODEL_PERSONALIZATION_PROMPT, TINY_LLAMA_MODEL_PERSONALIZATION_PROMPT
from app.model.gpt_2_model import GPT2Model
from app.model.helsinki_transalation_model import HelsinkiTransalationModel
from app.model.tiny_llama_model import TinyLlamaModel


class LlmManager:
    """
    Manager class for handling Large Language Model operations.

    This class manages different LLM models for personalizing horoscope content
    and handles translation services. It provides a unified interface for
    text generation and language translation operations with configurable
    translation models.

    Attributes:
        model_dict (Dict[LlmModelsEnum, Union[TinyLlamaModel, GPT2Model]]):
            Dictionary mapping model enums to model instances
        model_prompt_dict (Dict[LlmModelsEnum, str]):
            Dictionary mapping model enums to their specific prompts
        translator_dict (Dict[TranslatorModelsEnum, HelsinkiTransalationModel]):
            Dictionary mapping translator enums to translator instances
    """

    def __init__(self) -> None:
        """
        Initialize the LlmManager with available models and translation services.

        Sets up the available LLM models (TinyLlama and GPT2), their corresponding
        prompts, and the Helsinki translation model for language conversion.
        """
        self.model_dict: Dict[LlmModelsEnum, Union[TinyLlamaModel, GPT2Model]] = {
            LlmModelsEnum.TINY_LLAMA: TinyLlamaModel(),
            LlmModelsEnum.GPT2: GPT2Model(),
        }
        self.model_prompt_dict: Dict[LlmModelsEnum, str] = {
            LlmModelsEnum.TINY_LLAMA: TINY_LLAMA_MODEL_PERSONALIZATION_PROMPT,
            LlmModelsEnum.GPT2: GPT2_MODEL_PERSONALIZATION_PROMPT,
        }
        self.translator_dict: Dict[TranslatorModelsEnum, HelsinkiTransalationModel] = {
            TranslatorModelsEnum.HELSINKI: HelsinkiTransalationModel(),
        }

    @staticmethod
    def _clean_response(text: str) -> str:
        """
        Clean and normalize the response text from LLM models.

        This method removes unwanted formatting, extra whitespace, and common
        email signature patterns that might appear in generated text.

        Args:
            text (str): Raw text response from the LLM model

        Returns:
            str: Cleaned and normalized text

        Example:
            >>> LlmManager._clean_response("Hello\\nJohn,\\n\\nBest wishes,")
            "Hello John,"
        """
        # Replace newlines with spaces
        cleaned = text.replace("\\n", " ").replace("\n", " ")

        # Remove extra whitespace
        cleaned = " ".join(cleaned.split())

        # Remove unwanted endings (backup cleanup)
        unwanted_endings = ["Best wishes,", "[Your Name]", "Sincerely,", "Best regards,"]
        for ending in unwanted_endings:
            if ending in cleaned:
                cleaned = cleaned.split(ending)[0].strip()

        return cleaned.strip()

    def personalize_horoscope(
        self,
        horoscope: str,
        name: str,
        model: LlmModelsEnum = LlmModelsEnum.TINY_LLAMA,
        language: ResponseLanguageEnum = ResponseLanguageEnum.ENGLISH,
        translator: TranslatorModelsEnum = TranslatorModelsEnum.HELSINKI,
    ) -> str:
        """
        Personalize a horoscope text using AI models and optionally translate it.

        This method takes a generic horoscope text and personalizes it for a specific
        user using the specified LLM model. It can also translate the result to Hindi
        if requested using the Helsinki translation model.

        Args:
            horoscope (str): The generic horoscope text to personalize
            name (str): The user's name for personalization
            model (LlmModelsEnum, optional): The LLM model to use. Defaults to TINY_LLAMA
            language (ResponseLanguageEnum, optional): Target language. Defaults to ENGLISH
            translator (TranslatorModelsEnum, optional): Translation model to use. Defaults to HELSINKI

        Returns:
            str: Personalized horoscope text in the requested language

        Raises:
            KeyError: If the specified model or translator is not available
            Exception: If text generation or translation fails

        Example:
            >>> manager = LlmManager()
            >>> horoscope = "Today is a good day for new beginnings."
            >>> personalized = manager.personalize_horoscope(
            ...     horoscope=horoscope,
            ...     name="John",
            ...     model=LlmModelsEnum.TINY_LLAMA,
            ...     language=ResponseLanguageEnum.HINDI,
            ...     translator=TranslatorModelsEnum.HELSINKI,
            ... )
            >>> print(personalized)
            "जॉन, आज नई शुरुआत के लिए एक अच्छा दिन है..."
        """
        prompt: str = self.model_prompt_dict[model].format(horoscope=horoscope, name=name)
        llm_model: Union[TinyLlamaModel, GPT2Model] = self.model_dict[model]
        personalized_horoscope: str = llm_model.generate_personalized_test(prompt)
        personalized_horoscope = self._clean_response(personalized_horoscope)

        if language == ResponseLanguageEnum.HINDI:
            translation_model: HelsinkiTransalationModel = self.translator_dict[translator]
            personalized_horoscope = translation_model.translate_to_hindi(personalized_horoscope)

        return personalized_horoscope
