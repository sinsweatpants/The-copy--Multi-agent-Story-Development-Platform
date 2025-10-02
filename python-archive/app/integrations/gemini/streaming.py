import logging
from typing import Any, Dict, AsyncGenerator

from fastapi import WebSocket
from google.api_core import exceptions as google_exceptions

from app.integrations.gemini.client import GeminiClient
from app.utils.exceptions import GeminiAPIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiStreamHandler:
    """
    Handles streaming content generation from the Gemini API and broadcasting
    it over a WebSocket connection.
    """

    def __init__(self, gemini_client: GeminiClient):
        """
        Initializes the stream handler with a Gemini client instance.

        Args:
            gemini_client: An initialized GeminiClient.
        """
        if not isinstance(gemini_client, GeminiClient):
            raise TypeError("gemini_client must be an instance of GeminiClient")
        self.client = gemini_client

    async def stream_response(
        self,
        prompt: str,
        websocket: WebSocket,
        generation_config_dict: Dict[str, Any] = None
    ) -> None:
        """
        Generates content as a stream and sends each chunk over the WebSocket.

        Args:
            prompt: The text prompt to send to the model.
            websocket: The WebSocket connection to send messages to.
            generation_config_dict: A dictionary of generation parameters.

        Raises:
            GeminiAPIError: If the API stream fails.
        """
        try:
            logger.info(f"Starting Gemini stream for WebSocket: {websocket.client}")

            # Use the underlying model from the client to stream
            stream = await self.client.model.generate_content_async(
                prompt,
                generation_config=generation_config_dict,
                stream=True
            )

            async for chunk in stream:
                if chunk.text:
                    # Broadcast the chunk of text to the client
                    await websocket.send_json({
                        "type": "content_chunk",
                        "payload": chunk.text
                    })

            logger.info(f"Finished Gemini stream for WebSocket: {websocket.client}")

        except (google_exceptions.GoogleAPICallError, google_exceptions.RetryError) as e:
            error_message = f"A Google API streaming error occurred: {e}"
            logger.error(error_message, exc_info=True)
            await self._send_error_message(websocket, error_message)
            raise GeminiAPIError(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred during streaming: {e}"
            logger.error(error_message, exc_info=True)
            await self._send_error_message(websocket, error_message)
            raise GeminiAPIError(error_message)

    async def generate_and_yield_chunks(
        self,
        prompt: str,
        generation_config_dict: Dict[str, Any] = None
    ) -> AsyncGenerator[str, None]:
        """
        A generator that yields text chunks from the Gemini stream.
        Useful for non-WebSocket streaming scenarios.
        """
        try:
            stream = await self.client.model.generate_content_async(
                prompt,
                generation_config=generation_config_dict,
                stream=True
            )
            async for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Error yielding chunks from stream: {e}", exc_info=True)
            raise GeminiAPIError(f"Stream generation failed: {e}")

    async def _send_error_message(self, websocket: WebSocket, error_message: str):
        """Safely sends an error message over the WebSocket."""
        try:
            await websocket.send_json({
                "type": "error",
                "payload": error_message
            })
        except Exception as e:
            # This might happen if the websocket is already closed
            logger.warning(f"Could not send error message to client: {e}")