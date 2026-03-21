"""
LLM client for the web navigation agent.
Wraps the Google Generative AI SDK to send multimodal prompts (text + images)
and parse structured JSON actions from the response.
"""

from __future__ import annotations

import base64
import os
from typing import Any, Optional

from google import genai
from google.genai import types

from .action_space import AgentAction, ActionParseError, parse_action


DEFAULT_MODEL = "gemini-2.0-flash"
MAX_RETRIES = 3


class LLMClient:
    """Sends multimodal prompts to Gemini and parses structured action responses."""

    def __init__(self, model: str = DEFAULT_MODEL, api_key: Optional[str] = None):
        self.model = model
        key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise ValueError(
                "No API key found. Set GEMINI_API_KEY or GOOGLE_API_KEY env var, "
                "or pass api_key= to LLMClient."
            )
        self._client = genai.Client(api_key=key)

    async def get_action(
        self,
        messages: list[dict[str, Any]],
        screenshot_base64: Optional[str] = None,
    ) -> AgentAction:
        """
        Send the conversation to Gemini and parse the response as an AgentAction.

        messages: list of {"role": "user"|"model", "text": str}
        screenshot_base64: optional base64 PNG to attach to the latest user message
        """
        last_error: Optional[str] = None

        for attempt in range(MAX_RETRIES):
            contents = self._build_contents(messages, screenshot_base64, last_error)

            retry_tag = f" (retry {attempt})" if attempt > 0 else ""
            print(f"  [llm] Calling Gemini API{retry_tag}...")
            try:
                response = self._client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=1024,
                    ),
                )
                print(f"  [llm] Response received")
            except Exception as e:
                last_error = f"API call failed: {e}"
                print(f"  [llm] API error: {e}")
                continue

            response_text = response.text
            if not response_text:
                last_error = "Empty response from model"
                print(f"  [llm] Empty response from model")
                continue

            print(f"  [llm] Raw response ({len(response_text)} chars): {response_text[:200]}")
            try:
                action = parse_action(response_text)
                action.reasoning = action.reasoning or self._extract_reasoning(response_text)
                return action
            except ActionParseError as e:
                last_error = str(e)
                print(f"  [llm] Parse error: {e}")
                continue

        raise ActionParseError(
            f"Failed to get valid action after {MAX_RETRIES} attempts. Last error: {last_error}"
        )

    def _build_contents(
        self,
        messages: list[dict[str, Any]],
        screenshot_base64: Optional[str],
        retry_error: Optional[str],
    ) -> list[types.Content]:
        """Convert our message format to Gemini SDK Content objects."""
        contents: list[types.Content] = []

        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            parts = [types.Part.from_text(text=msg["text"])]
            contents.append(types.Content(role=role, parts=parts))

        if screenshot_base64:
            image_bytes = base64.b64decode(screenshot_base64)
            image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
            if contents and contents[-1].role == "user":
                contents[-1].parts.append(image_part)
            else:
                contents.append(types.Content(
                    role="user",
                    parts=[image_part],
                ))

        if retry_error:
            error_text = (
                f"Your previous response was not a valid action. Error: {retry_error}\n"
                "Please respond with a single JSON object with an 'action' field."
            )
            if contents and contents[-1].role == "user":
                contents[-1].parts.append(types.Part.from_text(text=error_text))
            else:
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=error_text)],
                ))

        return contents

    def _extract_reasoning(self, text: str) -> Optional[str]:
        """Try to extract reasoning from the model response text outside the JSON."""
        json_start = text.find("{")
        if json_start > 0:
            before_json = text[:json_start].strip()
            if len(before_json) > 10:
                return before_json
        return None
