import os

DIAL_URL = 'https://ai-proxy.lab.epam.com'
DIAL_CHAT_COMPLETIONS_ENDPOINT = DIAL_URL + '/openai/deployments/{model}/chat/completions'
API_KEY = os.getenv('DIAL_API_KEY', '')
#DEPLOYMENT_NAME = "gemini-2.5-pro"
DEPLOYMENT_NAME = "gpt-4o"
