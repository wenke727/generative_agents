import os
import re
import time
import csv
import inspect
import openai
from functools import wraps

from dotenv import load_dotenv
load_dotenv(".env", verbose=True)

GPT_35_TURBO = os.environ.get("BASE_MODEL", "gpt-35-turbo")
OPENAI_LOG_FILE = 'openai_api_log.csv'


def set_openai_api_log_file(fn):
    global OPENAI_LOG_FILE
    OPENAI_LOG_FILE = fn

    return True

def get_caller_function_name(pattern):
    """
    Recursively finds the name of the caller function that matches a given pattern.

    Args:
        pattern (str): The regex pattern to match the caller function name.

    Returns:
        str: The name of the matching caller function, or None if no match is found.
    """
    frame = inspect.currentframe()
    while frame:
        code = frame.f_code
        if re.search(pattern, code.co_name):
            return code.co_name
        frame = frame.f_back

    return None


def log_function_call(func, pattern = r"(?i)(run_gpt|ChatGPT_safe)"):
    """
    A decorator that logs the function call details including timestamp, caller function name,
    input arguments, and output result, and saves them to a CSV file.

    Args:
        func (callable): The function to be wrapped.

    Returns:
        callable: The wrapped function with logging functionality.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        caller = get_caller_function_name(pattern)
        # ms
        timestamp = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}.{int(time.time() * 1000) % 1000:03d}"

        input_data = {"args": args, "kwargs": kwargs}
        result = func(*args, **kwargs)
        output_data = result

        log_entry = {
            "timestamp": timestamp,
            "caller": caller,
            "input": input_data,
            "output": output_data
        }
        # print(log_entry)  # Here you can replace this with actual logging to a file or database

        # Save log entry to CSV file
        with open(OPENAI_LOG_FILE, 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'caller', 'input', 'output']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()  # Write header if file is empty

            writer.writerow(log_entry)

        return result

    return wrapper


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

    # Wrap chat and embeddings with logging
    chat = log_function_call(chat)
    # embeddings = log_function_call(embeddings)

    return client, chat, embeddings


if __name__ == "__main__":
    # Example usage:
    client, chat, embeddings = initialize_openai_client()
    response = chat(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello, world!"}])
    embedding = embeddings(input="Hello, world!")