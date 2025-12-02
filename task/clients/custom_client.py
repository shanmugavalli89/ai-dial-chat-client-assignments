import json
import aiohttp
import requests

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):
    _endpoint: str

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._endpoint = (
            DIAL_ENDPOINT
            + f"/openai/deployments/{deployment_name}/chat/completions"
        )

    # ============================================================
    # NON-STREAM COMPLETION
    # ============================================================
    def get_completion(self, messages: list[Message]) -> Message:

        # 1. Create headers dict
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }

        # 2. Create request_data dictionary
        request_data = {
            "messages": [m.to_dict() for m in messages]
        }

        # 3. POST request
        response = requests.post(
            self._endpoint,
            headers=headers,
            json=request_data
        )

        # 5. Error handling
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        data = response.json()

        # 4. Extract content
        choices = data.get("choices", None)
        if not choices:
            raise Exception("No choices found in response")

        content = choices[0]["message"]["content"]

        print(content)

        return Message(role=Role.AI, content=content)

    # ============================================================
    # STREAMING COMPLETION
    # ============================================================
    async def stream_completion(self, messages: list[Message]) -> Message:

        # 1. Create headers
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }

        # 2. Request data with streaming enabled
        request_data = {
            "stream": True,
            "messages": [m.to_dict() for m in messages]
        }

        # 3. Collect streamed content
        contents = []

        # 4. aiohttp session
        async with aiohttp.ClientSession() as session:

            # 5. POST request
            async with session.post(
                self._endpoint,
                json=request_data,
                headers=headers
            ) as resp:

                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}: {await resp.text()}")

                # 6. Stream chunks
                async for raw_chunk in resp.content:

                    line = raw_chunk.decode().strip()

                    # Expected format:  data: {...}
                    if not line.startswith("data: "):
                        continue

                    data_part = line[6:].strip()

                    # End of stream
                    if data_part == "[DONE]":
                        break

                    # Parse chunk
                    chunk_json = json.loads(data_part)
                    delta = chunk_json["choices"][0]["delta"]
                    content_piece = delta.get("content")

                    if content_piece:
                        print(content_piece, end="", flush=True)
                        contents.append(content_piece)

        # After stream ends, move to new line
        print()

        # Join everything into a final response
        final_content = "".join(contents)

        return Message(role=Role.AI, content=final_content)
