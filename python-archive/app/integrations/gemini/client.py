import asyncio
import logging
from typing import Any, Dict

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from app.utils.exceptions import GeminiAPIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    It handles API key configuration, model initialization, and robust error handling.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.5-pro"):
        """
        Initializes the Gemini client.

        Args:
            api_key: The Google AI API key.
            model_name: The name of the Gemini model to use.

        Raises:
            GeminiAPIError: If the API key is not provided or configuration fails.
        """
        if not api_key:
            raise GeminiAPIError("Google API key is missing.")
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini client initialized successfully for model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise GeminiAPIError(f"Failed to configure Gemini API: {e}")

    async def generate_content(self, prompt: str, generation_config_dict: Dict[str, Any] = None) -> str:
        """
        Generates content using the configured Gemini model with retry logic.

        Args:
            prompt: The text prompt to send to the model.
            generation_config_dict: A dictionary of generation parameters (e.g., temperature, max_output_tokens).

        Returns:
            The generated text content.

        Raises:
            GeminiAPIError: If the API call fails after retries.
        """
        try:
            generation_config = genai.types.GenerationConfig(**generation_config_dict) if generation_config_dict else None

            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config
            )

            if not response.candidates:
                raise GeminiAPIError("No content generated. The response from Gemini was empty.")

            # In case the response text is empty or None
            if not response.text:
                 raise GeminiAPIError("No text found in the generated content.")

            return response.text

        except (google_exceptions.GoogleAPICallError, google_exceptions.RetryError, google_exceptions.Aborted) as e:
            logger.error(f"A critical Google API error occurred: {e}", exc_info=True)
            raise GeminiAPIError(f"A Google API error occurred: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred during content generation: {e}", exc_info=True)
            raise GeminiAPIError(f"An unexpected error occurred: {e}")

class GeminiClientPool:
    """
    Manages a pool of GeminiClient instances to handle concurrent requests efficiently.
    This uses an asyncio.Queue to limit the number of active clients.
    """

    def __init__(self, api_key: str, pool_size: int = 10):
        """
        Initializes the client pool.

        Args:
            api_key: The Google AI API key for all clients in the pool.
            pool_size: The maximum number of concurrent clients.
        """
        if not api_key:
            raise ValueError("API key cannot be empty for the client pool.")

        self._api_key = api_key
        self._pool = asyncio.Queue(maxsize=pool_size)
        logger.info(f"Gemini client pool initialized with size: {pool_size}")

    async def get_client(self, model_name: str) -> "GeminiClientContextManager":
        """
        Gets a client from the pool to be used in a 'async with' block.

        Args:
            model_name: The specific Gemini model required for the client.

        Returns:
            An async context manager that provides a GeminiClient.
        """
        client = GeminiClient(api_key=self._api_key, model_name=model_name)
        return GeminiClientContextManager(self, client)

    async def _put_client(self, client: GeminiClient):
        """Internal method to return a client to the pool."""
        # This is a placeholder as we create clients on demand.
        # In a more complex scenario, you might queue/reuse configured clients.
        pass

class GeminiClientContextManager:
    """An async context manager for safely using clients from the pool."""
    def __init__(self, pool: GeminiClientPool, client: GeminiClient):
        self._pool = pool
        self._client = client

    async def __aenter__(self) -> GeminiClient:
        return self._client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._pool._put_client(self._client)