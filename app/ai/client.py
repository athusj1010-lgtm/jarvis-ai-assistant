from __future__ import annotations

import os
from typing import Any

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


class AIClient:
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini", base_url: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.client = None
        if OpenAI is not None and self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def is_available(self) -> bool:
        return self.client is not None

    def chat(self, system_prompt: str, user_text: str) -> str:
        if self.client is None:
            raise RuntimeError("AI client is not configured.")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return response.choices[0].message.content or ""


def build_ai_client(settings: Any) -> AIClient:
    return AIClient(api_key=settings.api_key, model=settings.ai_model, base_url=settings.base_url)
