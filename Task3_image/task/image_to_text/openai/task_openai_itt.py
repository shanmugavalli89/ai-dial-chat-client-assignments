import base64
from pathlib import Path

from task._utils.constants import (
    API_KEY,
    DIAL_CHAT_COMPLETIONS_ENDPOINT,
    DEPLOYMENT_NAME,
)
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import (
    ContentedMessage,
    TxtContent,
    ImgContent,
    ImgUrl,
)


def start() -> None:
    # --------------------------------------------------
    # Load image and convert to base64
    # --------------------------------------------------
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # --------------------------------------------------
    # Create DIAL model client (VISION model)
    # --------------------------------------------------
    print("Using deployment:", DEPLOYMENT_NAME)

    model_client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name=DEPLOYMENT_NAME,
        api_key=API_KEY,
    )

    # --------------------------------------------------
    # Create image-to-text request (base64 image)
    # --------------------------------------------------
    message = ContentedMessage(
        role=Role.USER,
        content=[
            TxtContent(text="What do you see in this picture?"),
            ImgContent(
                image_url=ImgUrl(
                    url=f"data:image/png;base64,{base64_image}"
                )
            ),
        ],
    )

    # --------------------------------------------------
    # Call model
    # --------------------------------------------------
    response = model_client.get_completion(messages=[message])

    print("\n================ MODEL RESPONSE ================\n")
    print(response)


if __name__ == "__main__":
    start()
