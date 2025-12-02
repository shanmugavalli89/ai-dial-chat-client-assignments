from aidial_client import Dial, AsyncDial
import os

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)

        api_key = os.getenv("DIAL_API_KEY")
        if not api_key:
            raise ValueError("Set DIAL_API_KEY environment variable")

        # Create Dial client (sync)
        self.client = Dial(
            base_url=DIAL_ENDPOINT,
            api_key=api_key
        )

        # Create Dial client (async)
        self.async_client = AsyncDial(
            base_url=DIAL_ENDPOINT,
            api_key=api_key
        )

    # ========================================================
    # Non-stream completion
    # ========================================================
    def get_completion(self, messages: list[Message]) -> Message:

        payload_messages = [m.to_dict() for m in messages]

        # NEW SYNTAX: MUST pass deployment_name
        response = self.client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=payload_messages,
            stream=False
        )

        content = response.choices[0].message.get("content", "")
        print(content)

        return Message(role=Role.AI, content=content)

    # ========================================================
    # Streaming completion (async)
    # ========================================================
    async def stream_completion(self, messages: list[Message]) -> Message:

        payload_messages = [m.to_dict() for m in messages]

        # NEW SYNTAX: MUST pass deployment_name
        stream = await self.async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=payload_messages,
            stream=True
        )

        chunks = []

        async for chunk in stream:
            delta = chunk.choices[0].delta
            part = delta.content or ""

            if part:
                print(part, end="", flush=True)
                chunks.append(part)

        print()
        full = "".join(chunks)
        return Message(role=Role.AI, content=full)
