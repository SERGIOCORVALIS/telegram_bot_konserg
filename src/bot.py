import asyncio
import logging
import os
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Final

from aiohttp import ClientError, ClientResponseError, ClientSession, ClientTimeout
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from dotenv import load_dotenv

OPENROUTER_URL: Final[str] = "https://openrouter.ai/api/v1/chat/completions"

# List of models for rotation on rate limit
AVAILABLE_MODELS: Final[list[str]] = [
    "google/gemini-2.0-flash-exp:free",
    "qwen/qwen3-coder:free",
    "qwen/qwen3-235b-a22b:free",
    "deepseek/deepseek-chat-v3.1:free",
]

# List of API keys for rotation
DEFAULT_API_KEYS: Final[list[str]] = [
    "REDACTED",
    "REDACTED",
    "REDACTED",
    "REDACTED",
    "REDACTED",
    "REDACTED",
    "REDACTED",
]

DEFAULT_TELEGRAM_TOKEN: Final[str] = ""
DEFAULT_OPENROUTER_API_KEY: Final[str] = DEFAULT_API_KEYS[0]
SYSTEM_PROMPT: Final[str] = (
    "You are a helpful AI assistant helping users in Telegram. "
    "Provide concise, well-structured answers in the language of the question. "
    "If the request is unclear, ask for clarification."
)


DEFAULT_APP_NAME: Final[str] = "AI Assistant Bot"
DEFAULT_REQUEST_TIMEOUT: Final[float] = 45.0
MAX_HISTORY_MESSAGES: Final[int] = 20  # Maximum number of messages in history
RATE_LIMIT_MESSAGES: Final[int] = 10  # Maximum messages
RATE_LIMIT_WINDOW: Final[int] = 60  # Time window (seconds)


@dataclass(slots=True)
class Settings:
    telegram_token: str
    openrouter_api_keys: list[str]
    app_public_url: str | None
    app_name: str
    request_timeout: float

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", DEFAULT_TELEGRAM_TOKEN)
        # Clean token: remove quotes and whitespace
        if telegram_token:
            telegram_token = telegram_token.strip().strip('"').strip("'")
        
        # Collect all available keys from environment variables
        api_keys: list[str] = []
        # Main key
        main_key = os.getenv("OPENROUTER_API_KEY", DEFAULT_OPENROUTER_API_KEY)
        if main_key:
            # Clean key: remove quotes and whitespace (same as token)
            main_key = main_key.strip().strip('"').strip("'")
            if main_key:
                api_keys.append(main_key)
        
        # Additional keys OPENROUTER_API_KEY_1, OPENROUTER_API_KEY_2, etc.
        for i in range(1, 10):  # Check up to 9 additional keys
            key = os.getenv(f"OPENROUTER_API_KEY_{i}")
            if key:
                # Clean key: remove quotes and whitespace
                key = key.strip().strip('"').strip("'")
                if key and key not in api_keys:
                    api_keys.append(key)
        
        # If no keys, use defaults
        if not api_keys:
            api_keys = DEFAULT_API_KEYS.copy()
        
        # Validate API keys format (OpenRouter keys should start with "sk-or-v1-")
        # Log warning for invalid keys but don't fail (might be valid custom format)
        for i, key in enumerate(api_keys):
            if key and not key.startswith("sk-or-v1-") and len(key) > 10:
                logging.warning(
                    "API Key %d doesn't match OpenRouter format (sk-or-v1-...): %s...%s",
                    i + 1,
                    key[:10],
                    key[-4:] if len(key) > 4 else "",
                )
        
        app_public_url = os.getenv("APP_PUBLIC_URL")
        app_name = os.getenv("APP_NAME", DEFAULT_APP_NAME)

        request_timeout_raw = os.getenv("REQUEST_TIMEOUT")
        try:
            request_timeout = float(request_timeout_raw) if request_timeout_raw else DEFAULT_REQUEST_TIMEOUT
        except ValueError as error:
            raise RuntimeError("REQUEST_TIMEOUT must be a numeric value") from error

        missing: list[str] = []
        if not telegram_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not api_keys:
            missing.append("OPENROUTER_API_KEY (or OPENROUTER_API_KEY_1, etc.)")
        if missing:
            error_msg = (
                f"Environment variables are required: {', '.join(missing)}\n\n"
                "Please add these variables in your deployment platform:\n"
                "- Railway: Go to your service → Variables tab → Add variables\n"
                "- Render: Go to your service → Environment → Add variables\n"
                "- Local: Create a .env file with these variables\n\n"
                "See RAILWAY_FIX_NOW.md for detailed instructions."
            )
            raise RuntimeError(error_msg)

        return cls(
            telegram_token=telegram_token,
            openrouter_api_keys=api_keys,
            app_public_url=app_public_url,
            app_name=app_name,
            request_timeout=request_timeout,
        )


class OpenRouterClient:
    def __init__(
        self,
        api_keys: list[str],
        *,
        app_public_url: str | None,
        app_name: str,
        models: list[str] | None = None,
    ) -> None:
        self.api_keys = api_keys
        self.models = models or AVAILABLE_MODELS.copy()
        self.app_public_url = app_public_url
        self.app_name = app_name

    def _build_headers(self, api_key: str) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.app_public_url:
            headers["HTTP-Referer"] = self.app_public_url
        headers["X-Title"] = self.app_name
        return headers

    async def complete(self, session: ClientSession, messages: list[dict[str, str]]) -> str:
        # Shuffle models and keys for even load distribution
        models = self.models.copy()
        keys = self.api_keys.copy()
        random.shuffle(models)
        random.shuffle(keys)

        last_error: Exception | None = None

        # Try all combinations of models and keys
        for model in models:
            for api_key in keys:
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.2,
                    "top_p": 0.95,
                }

                try:
                    async with session.post(
                        OPENROUTER_URL, headers=self._build_headers(api_key), json=payload
                    ) as response:
                        # If we got 429, try next combination
                        if response.status == 429:
                            logging.warning(
                                "Rate limited: model=%s, key=%s...%s",
                                model,
                                api_key[:10],
                                api_key[-4:],
                            )
                            await asyncio.sleep(0.5)  # Small delay before next attempt
                            continue

                        response.raise_for_status()
                        data: dict[str, Any] = await response.json()

                        choices = data.get("choices", [])
                        if not choices:
                            raise RuntimeError("OpenRouter response does not contain choices")

                        content = choices[0].get("message", {}).get("content")
                        if not isinstance(content, str):
                            raise RuntimeError("OpenRouter response content is not a string")

                        logging.info("Successfully used model=%s", model)
                        return content.strip()

                except ClientResponseError as error:
                    # Special handling for 401 (Unauthorized) - likely API key issue
                    if error.status == 401:
                        logging.error(
                            "❌ 401 Unauthorized - API key authentication failed!\n"
                            "   Model: %s\n"
                            "   Key preview: %s...%s (length: %d)\n"
                            "   Check: 1) Key is correct 2) No extra spaces/quotes 3) Key is active",
                            model,
                            api_key[:10],
                            api_key[-4:],
                            len(api_key),
                        )
                    # If not 429, try next combination
                    if error.status != 429:
                        logging.warning(
                            "Error %s with model=%s, key=%s...%s: %s",
                            error.status,
                            model,
                            api_key[:10],
                            api_key[-4:],
                            error.message,
                        )
                    last_error = error
                    continue
                except Exception as error:
                    last_error = error
                    logging.warning("Unexpected error with model=%s: %s", model, error)
                    continue

        # If all combinations failed, raise the last error
        if last_error:
            raise last_error
        raise RuntimeError("All models and keys exhausted")


class DialogHistory:
    """Dialog history management for each user."""

    def __init__(self, max_messages: int = MAX_HISTORY_MESSAGES) -> None:
        self.history: dict[int, list[dict[str, str]]] = defaultdict(list)
        self.max_messages = max_messages

    def get_messages(self, user_id: int) -> list[dict[str, str]]:
        """Get user's message history."""
        return self.history[user_id].copy()

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """Add message to user's history."""
        self.history[user_id].append({"role": role, "content": content})
        # Limit history size
        if len(self.history[user_id]) > self.max_messages:
            # Keep system prompt and latest messages
            system_msg = None
            if self.history[user_id] and self.history[user_id][0].get("role") == "system":
                system_msg = self.history[user_id][0]
            self.history[user_id] = self.history[user_id][-self.max_messages + 1 :]
            if system_msg:
                self.history[user_id].insert(0, system_msg)

    def clear_history(self, user_id: int) -> None:
        """Clear user's history."""
        if user_id in self.history:
            del self.history[user_id]

    def build_messages(self, user_id: int, system_prompt: str, user_message: str) -> list[dict[str, str]]:
        """Build message list with history (without saving new message)."""
        messages = self.get_messages(user_id)
        
        # If no history, add system prompt
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": system_prompt})
        elif messages[0].get("role") == "system":
            # Update system prompt if it changed
            messages[0]["content"] = system_prompt
        
        # Add new user message (only for request, don't save to history here)
        messages.append({"role": "user", "content": user_message})
        
        return messages


class RateLimiter:
    """Spam protection: limit number of requests from user."""

    def __init__(self, max_messages: int = RATE_LIMIT_MESSAGES, window: int = RATE_LIMIT_WINDOW) -> None:
        self.max_messages = max_messages
        self.window = window
        self.requests: dict[int, list[float]] = defaultdict(list)

    def check_rate_limit(self, user_id: int) -> tuple[bool, int]:
        """
        Check if request limit is exceeded.
        Returns (allowed, seconds until next request).
        """
        now = time.time()
        user_requests = self.requests[user_id]

        # Remove old requests (older than window)
        user_requests[:] = [req_time for req_time in user_requests if now - req_time < self.window]

        # Check limit
        if len(user_requests) >= self.max_messages:
            # Calculate time until next possible request
            oldest_request = min(user_requests)
            wait_time = int(self.window - (now - oldest_request)) + 1
            return False, wait_time

        # Add current request
        user_requests.append(now)
        return True, 0

    def reset(self, user_id: int) -> None:
        """Reset request counter for user."""
        if user_id in self.requests:
            del self.requests[user_id]


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def register_handlers(
    dp: Dispatcher,
    *,
    client: OpenRouterClient,
    session: ClientSession,
    dialog_history: DialogHistory,
    rate_limiter: RateLimiter,
) -> None:
    router = Router()

    @router.message(CommandStart())
    async def handle_start(message: Message) -> None:
        # Clear history and rate limit on start
        user_id = message.from_user.id
        dialog_history.clear_history(user_id)
        rate_limiter.reset(user_id)
        await message.answer(
            "Hello! I'm an AI assistant ready to answer your questions. "
            "Just send me your question.\n\n"
            "Use /reset to clear the dialog history."
        )

    @router.message(Command("help"))
    async def handle_help(message: Message) -> None:
        await message.answer(
            "📖 Available commands:\n\n"
            "/start - Start a dialog (clears history)\n"
            "/reset - Clear dialog history\n"
            "/about - Bot information\n"
            "/feedback - Send feedback\n\n"
            "Just send a text question and I'll try to answer. "
            "The bot remembers the context of previous messages in the dialog."
        )

    @router.message(Command("reset"))
    async def handle_reset(message: Message) -> None:
        user_id = message.from_user.id
        dialog_history.clear_history(user_id)
        rate_limiter.reset(user_id)
        await message.answer("✅ Dialog history cleared. You can start a new conversation!")

    @router.message(Command("about"))
    async def handle_about(message: Message) -> None:
        await message.answer(
            "🤖 AI Assistant Bot\n\n"
            "The bot uses multiple AI models via OpenRouter:\n"
            "• Google Gemini 2.0 Flash\n"
            "• Qwen3 Coder\n"
            "• Qwen3 235B\n"
            "• DeepSeek V3.1\n\n"
            "The bot automatically switches between models when overloaded.\n"
            "Dialog history is saved for contextual responses.\n\n"
            "Version: 1.0.0"
        )

    @router.message(Command("feedback"))
    async def handle_feedback(message: Message) -> None:
        await message.answer(
            "💬 Feedback and Suggestions\n\n"
            "If you have feedback or suggestions for improving the bot, "
            "just send a message with 'feedback:' at the beginning.\n\n"
            "Example: feedback: The bot works great!"
        )

    @router.message(F.text & ~F.via_bot)
    async def handle_question(message: Message) -> None:
        user_message = (message.text or "").strip()
        if not user_message:
            await message.answer("The message appears to be empty. Please send your question again.")
            return

        user_id = message.from_user.id

        # Check rate limit
        allowed, wait_time = rate_limiter.check_rate_limit(user_id)
        if not allowed:
            await message.answer(
                f"⏱ Too many requests! Please wait {wait_time} seconds "
                f"before sending another message.\n\n"
                f"Limit: {RATE_LIMIT_MESSAGES} messages per {RATE_LIMIT_WINDOW} seconds."
            )
            return

        # Build messages with history
        messages = dialog_history.build_messages(user_id, SYSTEM_PROMPT, user_message)

        try:
            async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
                reply_text = await client.complete(session, messages)
            
            # Save messages to history only after successful response
            dialog_history.add_message(user_id, "user", user_message)
            dialog_history.add_message(user_id, "assistant", reply_text)
            
        except ClientResponseError as error:
            logging.exception("OpenRouter returned an error: %s", error)
            if error.status == 429:
                reply_text = (
                    "All free models are temporarily overloaded (rate limit). "
                    "The bot automatically tries other models and keys. "
                    "Please try again in a few seconds."
                )
            else:
                reply_text = (
                    f"Failed to get response from model (error {error.status}). "
                    "Please try again a bit later."
                )
        except ClientError as error:
            logging.exception("Network error while talking to OpenRouter: %s", error)
            reply_text = (
                "A network error occurred while contacting the model. "
                "Check your connection and try again."
            )
        except Exception as error:  # noqa: BLE001
            logging.exception("Unexpected error while processing request: %s", error)
            reply_text = (
                "An unexpected error occurred. I'm already working on fixing it. "
                "Please try again a bit later."
            )

        await message.answer(reply_text)

    dp.include_router(router)


async def main() -> None:
    setup_logging()
    settings = Settings.from_env()

    try:
        bot = Bot(token=settings.telegram_token, parse_mode=None)
    except Exception as error:
        error_msg = str(error)
        if "Token is invalid" in error_msg or "TokenValidationError" in error_msg:
            logging.error(
                "Invalid Telegram bot token! Please check:\n"
                "1. Token format: should be like '123456789:ABCdefGHIjklMNOpqrsTUVwxyz'\n"
                "2. No extra spaces or quotes in Railway Variables\n"
                "3. Token is correct (get new one from @BotFather if needed)\n"
                "Current token (first 10 chars): %s...",
                settings.telegram_token[:10] if settings.telegram_token else "EMPTY",
            )
            raise RuntimeError(
                "Invalid Telegram bot token!\n\n"
                "Please check:\n"
                "1. Token format in Railway Variables (no quotes, no spaces)\n"
                "2. Token should be: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz\n"
                "3. Get a new token from @BotFather if needed\n\n"
                "In Railway: Go to Variables → Check TELEGRAM_BOT_TOKEN value"
            ) from error
        raise
    dp = Dispatcher()
    client = OpenRouterClient(
        settings.openrouter_api_keys,
        app_public_url=settings.app_public_url,
        app_name=settings.app_name,
    )

    # Initialize dialog history and spam protection
    dialog_history = DialogHistory()
    rate_limiter = RateLimiter()

    logging.info("Loaded %d API keys and %d models", len(settings.openrouter_api_keys), len(AVAILABLE_MODELS))
    # Log API key info for debugging (first 10 and last 4 chars, length)
    for i, key in enumerate(settings.openrouter_api_keys[:3], 1):  # Log first 3 keys
        logging.info("API Key %d: %s...%s (length: %d)", i, key[:10], key[-4:], len(key))
    if len(settings.openrouter_api_keys) > 3:
        logging.info("... and %d more API keys", len(settings.openrouter_api_keys) - 3)
    logging.info("Telegram token: %s...%s (length: %d)", 
                 settings.telegram_token[:10] if settings.telegram_token else "EMPTY",
                 settings.telegram_token[-4:] if settings.telegram_token and len(settings.telegram_token) > 4 else "",
                 len(settings.telegram_token) if settings.telegram_token else 0)
    logging.info("Rate limit: %d messages per %d seconds", RATE_LIMIT_MESSAGES, RATE_LIMIT_WINDOW)
    timeout = ClientTimeout(total=settings.request_timeout)
    async with ClientSession(timeout=timeout) as session:
        register_handlers(
            dp,
            client=client,
            session=session,
            dialog_history=dialog_history,
            rate_limiter=rate_limiter,
        )
        logging.info("Starting bot polling")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")

