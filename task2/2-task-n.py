import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task.app.main import run

# TODO:
#  Try the `n` parameter with different models (`deployment_name`). With the parameter `n`, we can configure how many
#       chat completion choices to generate for each input message
#  User massage: Why is the snow white?

# Models to try:
# - gpt-4o
# - claude-3-7-sonnet@20250219
# - gemini-2.5-pro

run(
    deployment_name='gemini-2.5-pro',
    n=5,
    print_request=False, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response
)

# Pay attention to the number of choices in the response!
# If you have worked with ChatGPT, you have probably seen responses where ChatGPT offers you a choice between two
# responses to select which one you prefer. This is done with the `n` parameter.
