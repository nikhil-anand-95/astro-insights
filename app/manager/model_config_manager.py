"""
Author: nikhil.anand
Created at: 20/07/25
"""

from app.config.model_definitions import MODEL_CONFIGURATIONS, TRANSLATOR_CONFIGURATIONS


class ModelConfigManager:
    """
    Manager class for handling model and translator configurations.

    This class provides centralized management of model configurations,
    allowing for dynamic enabling/disabling of models and translators
    based on configuration settings.
    """

    def __init__(self) -> None:
        """
        Initialize the ModelConfigManager with model and translator configurations.

        Loads the predefined configurations for all available models and translators.
        """
        self.model_configs = MODEL_CONFIGURATIONS
        self.translator_configs = TRANSLATOR_CONFIGURATIONS

    def get_enabled_models(self) -> list:
        """
        Get list of all enabled model configurations.

        Returns:
            list: List of enabled model configurations
        """
        return [config for config in self.model_configs.values() if config.enabled]

    def get_enabled_translators(self) -> list:
        """
        Get list of all enabled translator configurations.

        Returns:
            list: List of enabled translator configurations
        """
        return [config for config in self.translator_configs.values() if config.enabled]
