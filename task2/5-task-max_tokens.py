import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task.app.main import run

# TODO:
#  Try `max_tokens` parameter. It sets the maximum length of the AI's response. The AI will stop generating text once it hits this limit.
#  User massage: What is token when we are working with LLM?

run(
    deployment_name='gpt-4o',
    max_tokens=50,
    # TODO:
    #  Use `max_tokens` parameter with value 10
)

# Previously, we have seen that the `finish_reason` in choice was `stop`, but now it is `length`, and if you check the
# `content,` it is clearly unfinished.