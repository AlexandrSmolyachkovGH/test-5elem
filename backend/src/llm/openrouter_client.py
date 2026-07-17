"""OpenRouter client."""

import json
from pprint import pprint
from typing import (
    Any,
    AsyncIterator,
)

import httpx

from src.exceptions.custom_exceptions import LLMException
from src.models import Message
from src.settings import settings


class OpenRouterClient:
    """OpenRouter client."""

    def _get_headers(
        self,
    ) -> dict[str, str]:
        """Build request headers."""
        return {
            "Authorization": f"Bearer {settings.llm_settings.LLM_API_KEY}",
        }

    def _build_request_payload(
        self,
        model: str,
        messages: list[Message],
    ) -> dict[str, Any]:
        """Build request payload."""
        payload = [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in messages
        ]
        payload.reverse()

        return {
            "model": model,
            "messages": payload,
            "stream": True,
        }

    def _parse_line(
        self,
        line: str,
    ) -> str | None:
        """
        Take line like part of stream response.
        Parse it. If line contains message - return it.
        """
        if not line:
            return None

        if line.startswith(':'):
            return None

        if not line.startswith("data: "):
            return None

        try:
            event_data = line[6:]
            data_obj = json.loads(event_data)
            pprint(data_obj)
            content = data_obj["choices"][0]["delta"].get("content", None)
            if content:
                return content

        except json.JSONDecodeError as err:
            raise LLMException(
                message=str(err),
            ) from err

    async def stream_chat(
        self,
        model: str,
        messages: list[Message],
    ) -> AsyncIterator[str]:
        """Stream chat."""
        headers = self._get_headers()
        data = self._build_request_payload(
            model=model,
            messages=messages,
        )

        async with httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=settings.llm_settings.LLM_CONNECT_TIMEOUT,
                read=settings.llm_settings.LLM_READ_TIMEOUT,
                write=settings.llm_settings.LLM_WRITE_TIMEOUT,
                pool=settings.llm_settings.LLM_POOL_TIMEOUT,
            )
        ) as client:
            async with client.stream(
                method="POST",
                url=settings.llm_settings.LLM_URL,
                headers=headers,
                json=data,
            ) as response:
                if not response.is_success:
                    await response.aread()

                    error = response.json().get("error", {})
                    message = error.get("message", "Unknown LLM error.")
                    code = error.get("code", None)

                    raise LLMException(
                        message=message,
                        code=code,
                        status_code=response.status_code,
                    )

                async for line in response.aiter_lines():
                    if line == "data: [DONE]":
                        return

                    content: str | None = self._parse_line(
                        line=line,
                    )

                    if content is not None:
                        yield content


openrouter_client: OpenRouterClient = OpenRouterClient()
