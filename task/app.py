import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


# -----------------------------------------------------------
# CustomDialClient: DialClient + Logging
# -----------------------------------------------------------
class CustomDialClient(DialClient):

    def get_completion(self, messages):
        print("\n===== REQUEST =====")
        for m in messages:
            print(m.to_dict())

        msg = super().get_completion(messages)

        print("\n===== RESPONSE =====")
        print(msg.to_dict())
        print("====================\n")

        return msg

    async def stream_completion(self, messages):
        print("\n===== REQUEST =====")
        for m in messages:
            print(m.to_dict())

        msg = await super().stream_completion(messages)

        print("\n===== RESPONSE =====")
        print(msg.to_dict())
        print("====================\n")

        return msg


# -----------------------------------------------------------
# Main Loop
# -----------------------------------------------------------
async def start(stream: bool) -> None:

    # -----------------------------
    # 1. Deployment name
    # -----------------------------
    deployment_name = input("Enter deployment name: ").strip()
    if not deployment_name:
        print("You must enter a model deployment name!")
        return

    # -----------------------------
    # 1.1 Normal DialClient
    # -----------------------------
    client = DialClient(deployment_name)

    # -----------------------------
    # 1.2 CustomDialClient (with logs)
    # -----------------------------
    custom_client = CustomDialClient(deployment_name)

    # Choose active client
    active = custom_client
    print("\nUsing CustomDialClient (full logging enabled)\n")

    # -----------------------------
    # 2. Create Conversation
    # -----------------------------
    conversation = Conversation()

    # -----------------------------
    # 3. System prompt setup
    # -----------------------------
    system_prompt = input(
        "Enter system prompt (press Enter for default): "
    ).strip()

    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    # Add system message
    conversation.messages.append(
        Message(role=Role.SYSTEM, content=system_prompt)
    )

    print("\nSystem prompt added. Starting conversation...\n")

    # -----------------------------
    # 4. Chat Loop
    # -----------------------------
    while True:
        user_input = input("You: ").strip()

        # -----------------------------
        # 5. Exit condition
        # -----------------------------
        if user_input.lower() == "exit":
            print("Exiting...")
            return

        # -----------------------------
        # 6. Add user message to history
        # -----------------------------
        user_msg = Message(role=Role.USER, content=user_input)
        conversation.messages.append(user_msg)

        # -----------------------------
        # 7. Call streaming or non-streaming completion
        # -----------------------------
        if stream:
            assistant_msg = await active.stream_completion(
                conversation.messages
            )
        else:
            assistant_msg = active.get_completion(conversation.messages)

        # -----------------------------
        # 8. Add assistant reply to history
        # -----------------------------
        conversation.messages.append(assistant_msg)


# -----------------------------------------------------------
# Start Application
# -----------------------------------------------------------
asyncio.run(start(True))
