from dotenv import load_dotenv
load_dotenv(".env", verbose=True)

import os
import openai

GPT_35_TURBO = "gpt-3.5-turbo"
# GPT_35_TURBO = "gpt-3.5-turbo"


def initialize_openai_client():
    """
    Initialize the OpenAI client based on the available environment variables.

    Returns:
        completions: The completion client object.
        embeddings: The embeddings client object.
        chat: The chat completion create function (if applicable).
    """
    openai_version = int(openai.__version__.split(".")[0])

    if openai_version == 0:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        client = None
        chat = openai.ChatCompletion.create
        embeddings = openai.Embedding.create
    else:
        azure_api_key = os.getenv('AZURE_OPENAI_API_KEY')

        if azure_api_key:
            client = openai.AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("OPENAI_API_VERSION"),
            )
        else:
            client = openai.OpenAI()

        chat = client.chat.completions.create
        embeddings = client.embeddings.create

    return client, chat, embeddings

