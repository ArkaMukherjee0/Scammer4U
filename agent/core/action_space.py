"""
Defines the action space for the web navigation agent.
Each action is a structured dict the VLM outputs as JSON.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional


ACTION_SCHEMA: dict[str, dict[str, str]] = {
    "click": {"element_id": "int"},
    "type": {"element_id": "int", "text": "str"},
    "select_option": {"element_id": "int", "value": "str"},
    "check": {"element_id": "int", "checked": "bool"},
    "upload_file": {"element_id": "int", "file_key": "str"},
    "scroll": {"direction": "str", "amount": "int"},
    "navigate": {"url": "str"},
    "go_back": {},
    "switch_tab": {"tab_index": "int"},
    "close_tab": {"tab_index": "int"},
    "screenshot": {},
    "wait": {"seconds": "int"},
    "done": {"summary": "str"},
}

VALID_SCROLL_DIRECTIONS = {"up", "down"}

TYPE_VALIDATORS: dict[str, type] = {
    "int": int,
    "str": str,
    "bool": bool,
}


@dataclass
class AgentAction:
    action_type: str
    params: dict[str, Any] = field(default_factory=dict)
    reasoning: Optional[str] = None

    @property
    def element_id(self) -> Optional[int]:
        return self.params.get("element_id")

    @property
    def text(self) -> Optional[str]:
        return self.params.get("text")

    @property
    def summary(self) -> Optional[str]:
        return self.params.get("summary")

    def to_dict(self) -> dict:
        d = {"action": self.action_type, **self.params}
        if self.reasoning:
            d["reasoning"] = self.reasoning
        return d


class ActionParseError(Exception):
    pass


def parse_action(raw: str | dict) -> AgentAction:
    """Parse raw VLM output into a validated AgentAction."""
    if isinstance(raw, str):
        raw = _extract_json(raw)

    if not isinstance(raw, dict):
        raise ActionParseError(f"Expected a JSON object, got {type(raw).__name__}")

    action_type = raw.get("action")
    if not action_type or action_type not in ACTION_SCHEMA:
        valid = ", ".join(sorted(ACTION_SCHEMA.keys()))
        raise ActionParseError(
            f"Missing or invalid 'action' field. Got: {action_type!r}. "
            f"Valid actions: {valid}"
        )

    reasoning = raw.get("reasoning")
    schema = ACTION_SCHEMA[action_type]
    params: dict[str, Any] = {}

    for param_name, param_type_str in schema.items():
        value = raw.get(param_name)
        if value is None:
            raise ActionParseError(
                f"Action '{action_type}' requires parameter '{param_name}'"
            )
        expected_type = TYPE_VALIDATORS[param_type_str]
        if not isinstance(value, expected_type):
            if expected_type is int and isinstance(value, float) and value == int(value):
                value = int(value)
            elif expected_type is bool and isinstance(value, (int, str)):
                value = bool(value)
            else:
                raise ActionParseError(
                    f"Parameter '{param_name}' for action '{action_type}' "
                    f"must be {param_type_str}, got {type(value).__name__}"
                )
        params[param_name] = value

    if action_type == "scroll" and params.get("direction") not in VALID_SCROLL_DIRECTIONS:
        raise ActionParseError(
            f"scroll direction must be 'up' or 'down', got {params['direction']!r}"
        )

    if action_type == "wait":
        secs = params.get("seconds", 0)
        if secs < 0 or secs > 30:
            raise ActionParseError(f"wait seconds must be 0-30, got {secs}")

    return AgentAction(action_type=action_type, params=params, reasoning=reasoning)


def _extract_json(text: str) -> dict:
    """Extract JSON from VLM text output, handling markdown code fences."""
    text = text.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        start = 1
        end = len(lines)
        for i in range(1, len(lines)):
            if lines[i].strip() == "```":
                end = i
                break
        text = "\n".join(lines[start:end]).strip()

    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start == -1 or brace_end == -1:
        raise ActionParseError(f"No JSON object found in response: {text[:200]}")

    json_str = text[brace_start : brace_end + 1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ActionParseError(f"Invalid JSON: {e}. Raw: {json_str[:200]}")


def get_action_prompt_description() -> str:
    """Return a description of available actions for the system prompt."""
    lines = [
        "Available actions (respond with exactly one JSON object):\n",
    ]
    descriptions = {
        "click": 'Click an element (button, link, checkbox, radio). Example: {"action": "click", "element_id": 3}',
        "type": 'Type text into an input/textarea field. Example: {"action": "type", "element_id": 5, "text": "hello"}',
        "select_option": 'Select an option from a dropdown. Use the option value. Example: {"action": "select_option", "element_id": 7, "value": "masters"}',
        "check": 'Check or uncheck a checkbox. Example: {"action": "check", "element_id": 9, "checked": true}',
        "upload_file": 'Upload a file (e.g. resume). Use a file_key from the user profile. Example: {"action": "upload_file", "element_id": 11, "file_key": "resume"}',
        "scroll": 'Scroll the page. Example: {"action": "scroll", "direction": "down", "amount": 3}',
        "navigate": 'Navigate to a URL. Example: {"action": "navigate", "url": "http://example.com"}',
        "go_back": 'Go back to previous page. Example: {"action": "go_back"}',
        "switch_tab": 'Switch to another browser tab. Example: {"action": "switch_tab", "tab_index": 1}',
        "close_tab": 'Close a browser tab. Example: {"action": "close_tab", "tab_index": 2}',
        "screenshot": 'Take a screenshot to see the page visually. The image will appear in your next observation. Example: {"action": "screenshot"}',
        "wait": 'Wait for the page to update. Example: {"action": "wait", "seconds": 2}',
        "done": 'Declare the task complete. Example: {"action": "done", "summary": "Applied for the job successfully."}',
    }
    for action, desc in descriptions.items():
        lines.append(f"  - {desc}")
    lines.append("")
    lines.append('You may include a "reasoning" field to explain your thinking.')
    return "\n".join(lines)
