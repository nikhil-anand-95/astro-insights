"""
Author: nikhil.anand
Created at: 19/07/25
"""

from typing import List, Dict, Any
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline, Pipeline


class HelsinkiTransalationModel:
    """
    Helsinki translation model wrapper for English to Hindi translation.

    This class provides an interface to the Helsinki-NLP OPUS machine translation
    model specifically for translating English text to Hindi. It uses the
    pre-trained opus-mt-en-hi model for accurate translation.

    Attributes:
        translator (Pipeline): Hugging Face transformers pipeline for translation
    """

    def __init__(self) -> None:
        """
        Initialize the Helsinki translation model with English to Hindi pipeline.

        Sets up the Helsinki-NLP OPUS model and tokenizer for English to Hindi
        translation using the transformers pipeline interface.
        """
        model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-hi", use_safetensors=True)
        tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
        self.translator: Pipeline = pipeline("translation", model=model, tokenizer=tokenizer)

    def translate_to_hindi(self, text: str) -> str:
        """
        Translate English text to Hindi.

        This method takes English text as input and returns the Hindi translation
        using the Helsinki-NLP OPUS machine translation model.

        Args:
            text (str): The English text to be translated to Hindi

        Returns:
            str: The translated text in Hindi

        Raises:
            Exception: If translation fails or model is not properly initialized
            ValueError: If the input text is empty or invalid
        """
        result: List[Dict[str, Any]] = self.translator(text)
        return result[0]["translation_text"]
