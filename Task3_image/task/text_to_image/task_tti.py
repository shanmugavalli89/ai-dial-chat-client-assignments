import asyncio
from datetime import datetime
from pathlib import Path

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT, DIAL_URL
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


class Size:
    square: str = "1024x1024"
    height_rectangle: str = "1024x1792"
    width_rectangle: str = "1792x1024"


class Style:
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    standard: str = "standard"
    hd: str = "hd"


async def _save_images(attachments: list[Attachment]):
    output_dir = Path(__file__).parent / "generated_images"
    output_dir.mkdir(exist_ok=True)

    async with DialBucketClient(
        api_key=API_KEY,
        base_url=DIAL_URL
    ) as bucket_client:

        for idx, attachment in enumerate(attachments, start=1):
            image_bytes = await bucket_client.get_file(attachment.url)

            file_name = f"generated_{idx}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = output_dir / file_name

            with open(file_path, "wb") as f:
                f.write(image_bytes)

            print(f"✅ Image saved: {file_path}")

async def _run():
    model_client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="imagegeneration@005",
        api_key=API_KEY,
    )

    message = Message(
        role=Role.USER,
        content="Sunny day on Bali beach with palm trees and blue sky"
    )

    response = model_client.get_completion(
        messages=[message]
    )

    if response.custom_content and response.custom_content.attachments:
        await _save_images(response.custom_content.attachments)
    else:
        print("❌ No images returned")

def start() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    start()
