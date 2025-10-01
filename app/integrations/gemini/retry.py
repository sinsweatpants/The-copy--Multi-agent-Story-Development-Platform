import asyncio
import logging
import random
from functools import wraps
from typing import Callable, Any, Coroutine

from app.utils.exceptions import GeminiAPIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_with_exponential_backoff(
    retries: int = 5,
    backoff_in_seconds: float = 1,
    max_backoff_in_seconds: float = 16,
    jitter: bool = True,
    catch_exceptions: Any = (GeminiAPIError,)
) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    A decorator that provides an exponential backoff retry mechanism for async functions.

    Args:
        retries: The maximum number of retries.
        backoff_in_seconds: The initial backoff delay.
        max_backoff_in_seconds: The maximum possible backoff delay.
        jitter: If True, adds a random factor to the backoff time to prevent thundering herd.
        catch_exceptions: A tuple of exception types to catch and trigger a retry.
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that implements the retry logic.
            """
            current_retries = 0
            current_backoff = backoff_in_seconds

            while current_retries < retries:
                try:
                    # Attempt to execute the decorated function
                    return await func(*args, **kwargs)

                except catch_exceptions as e:
                    current_retries += 1

                    # If we have exhausted all retries, re-raise the last exception
                    if current_retries >= retries:
                        logger.error(
                            f"Function '{func.__name__}' failed after {retries} retries. Raising last exception: {e}",
                            exc_info=True
                        )
                        raise

                    # Calculate sleep time
                    sleep_time = current_backoff
                    if jitter:
                        sleep_time += random.uniform(0, current_backoff * 0.5)

                    logger.warning(
                        f"Function '{func.__name__}' failed with {type(e).__name__}. "
                        f"Retrying in {sleep_time:.2f} seconds... ({current_retries}/{retries})"
                    )

                    await asyncio.sleep(sleep_time)

                    # Exponentially increase the backoff time for the next potential failure
                    current_backoff = min(current_backoff * 2, max_backoff_in_seconds)

        return wrapper
    return decorator

# Example of how to use the decorator:
#
# @retry_with_exponential_backoff(retries=3, backoff_in_seconds=2)
# async def potentially_failing_api_call():
#     # ... code that might raise GeminiAPIError ...
#     pass