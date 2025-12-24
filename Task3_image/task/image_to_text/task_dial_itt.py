import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DEPLOYMENT_NAME, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'

    # 1. Create DialBucketClient
    async with DialBucketClient(
        api_key=API_KEY,
        base_url=DIAL_URL,
    ) as client:

        # 2. Open image file
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        # 3. Use BytesIO to load bytes of image
        content = BytesIO(image_bytes)

        # 4. Upload file with client
        response = await client.put_file(
            name=file_name,
            mime_type=mime_type_png,
            content=content,
        )

    # 5. Return Attachment object
    return Attachment(
        title=file_name,
        url=response["url"],
        type=mime_type_png,
    )


import asyncio

def start() -> None:
    async def _run():
        # 1. Upload image (ASYNC bucket client)
        attachment = await _put_image()
        print("Uploaded attachment:", attachment)

        # 2. Prepare message
        message = Message(
            role=Role.USER,
            content="What do you see on this picture?",
            custom_content=CustomContent(
                attachments=[attachment]
            ),
        )

        # 3. Create model client (SYNC)
        model_client = DialModelClient(
            endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
            deployment_name=DEPLOYMENT_NAME,
            api_key=API_KEY,
        )

        # 4. Call model (SYNC)
        response = model_client.get_completion(
            messages=[message]
        )

        print("Final model response:")
        print(response)

    asyncio.run(_run())


start()
