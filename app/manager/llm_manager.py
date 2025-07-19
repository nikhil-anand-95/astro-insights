"""
Author: nikhil.anand
Created at: 19/07/25
"""

from fastapi.logger import logger

from app.constants.enum import LlmModelsEnum, ResponseLanguageEnum, TranslatorModelsEnum
from app.manager.model_config_manager import ModelConfigManager
from app.model.gpt_2_model import GPT2Model
from app.model.helsinki_transalation_model import HelsinkiTransalationModel
from app.model.tiny_llama_model import TinyLlamaModel


class LlmManager:
    """
    Manager class for handling Large Language Model operations.

    This class manages different LLM models for personalizing horoscope content
    and handles translation services. It provides a unified interface for
    text generation and language translation operations with configuration-driven
    model management.

    Attributes:
        config_manager (ModelConfigManager): Configuration manager for models and translators
        model_dict (dict): Dictionary mapping model enums to loaded model instances
        model_prompt_dict (dict): Dictionary mapping model enums to their specific prompts
        translator_dict (dict): Dictionary mapping translator enums to loaded translator instances
    """

    def __init__(self) -> None:
        """
        Initialize the LlmManager with configuration-driven model loading.

        Loads only the enabled models and translators based on configuration settings,
        providing dynamic model management with enabled/disabled flags.
        """
        self.config_manager = ModelConfigManager()
        self.model_dict = self._load_enabled_models()
        self.model_prompt_dict = self._load_enabled_prompts()
        self.translator_dict = self._load_enabled_translators()

    def _load_enabled_models(self) -> dict:
        """
        Load only enabled models based on configuration.

        Returns:
            dict: Dictionary of loaded model instances
        """
        enabled_models = {}
        for config in self.config_manager.get_enabled_models():
            try:
                model_instance = self._create_model_instance(config.model_type)
                enabled_models[config.model_type] = model_instance
                logger.info(f"Successfully loaded model: {config.model_type.value}")
            except Exception as e:
                logger.error(f"Failed to load model {config.model_type.value}: {e}")
        return enabled_models

    def _load_enabled_prompts(self) -> dict:
        """
        Load prompts for enabled models based on configuration.

        Returns:
            dict: Dictionary mapping model types to their prompts
        """
        return {config.model_type: config.prompt for config in self.config_manager.get_enabled_models()}

    def _load_enabled_translators(self) -> dict:
        """
        Load only the enabled translators based on configuration.

        Returns:
            dict: Dictionary of loaded translator instances
        """
        enabled_translators = {}
        for config in self.config_manager.get_enabled_translators():
            try:
                translator_instance = self._create_translator_instance(config.translator_type)
                enabled_translators[config.translator_type] = translator_instance
                logger.info(f"Successfully loaded translator: {config.translator_type.value}")
            except Exception as e:
                logger.error(f"Failed to load translator {config.translator_type.value}: {e}")
        return enabled_translators

    @staticmethod
    def _create_model_instance(model_type: LlmModelsEnum):
        """
        Create a model instance based on the model type.

        Args:
            model_type (LlmModelsEnum): The type of model to create

        Returns:
            The created model instance

        Raises:
            KeyError: If the model type is not supported
        """
        model_mapping = {
            LlmModelsEnum.TINY_LLAMA: TinyLlamaModel,
            LlmModelsEnum.GPT2: GPT2Model,
        }
        if model_type not in model_mapping:
            raise KeyError(f"Unsupported model type: {model_type.value}")
        return model_mapping[model_type]()

    @staticmethod
    def _create_translator_instance(translator_type: TranslatorModelsEnum):
        """
        Create a translator instance based on the translator type.

        Args:
            translator_type (TranslatorModelsEnum): The type of translator to create

        Returns:
            The created translator instance

        Raises:
            KeyError: If the translator type is not supported
        """
        translator_mapping = {
            TranslatorModelsEnum.HELSINKI: HelsinkiTransalationModel,
        }
        if translator_type not in translator_mapping:
            raise KeyError(f"Unsupported translator type: {translator_type.value}")
        return translator_mapping[translator_type]()

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
        """
        prompt = self.model_prompt_dict[model].format(horoscope=horoscope, name=name)
        llm_model = self.model_dict[model]
        personalized_horoscope = llm_model.generate_personalized_test(prompt)
        personalized_horoscope = self._clean_response(personalized_horoscope)

        if language == ResponseLanguageEnum.HINDI:
            translation_model = self.translator_dict[translator]
            personalized_horoscope = translation_model.translate_to_hindi(personalized_horoscope)

        return personalized_horoscope
