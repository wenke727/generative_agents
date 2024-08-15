import os
import sys
import pytest
from loguru import logger
sys.path.append("./backend_server")

from dotenv import load_dotenv
load_dotenv('./backend_server/.env')

from persona.prompt_template.gpt_structure import (
    generate_prompt,
    safe_generate_response,
    ChatGPT_safe_generate_response,
    GPT_35_TURBO,
)

@pytest.fixture
def gpt_parameters():
    return {
        "engine": GPT_35_TURBO,
        "max_tokens": 50,
        "temperature": 0,
        "top_p": 1,
        "stream": False,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ['"'],
    }


def test_case_0(gpt_parameters):
    curr_input = ["driving to a friend's house"]
    prompt_lib_file = "./backend_server/persona/prompt_template//v1/test_prompt_July5.txt"
    prompt = generate_prompt(curr_input, prompt_lib_file)

    def __func_validate(gpt_response, prompt):
        if len(gpt_response.strip()) <= 1:
            return False
        if len(gpt_response.strip().split(" ")) > 1:
            return False
        return True

    def __func_clean_up(gpt_response, prompt):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    output = safe_generate_response(
        prompt, gpt_parameters, 5, "rest", __func_validate, __func_clean_up, True
    )
    logger.info(output)

    assert str.lower(output) == "visiting"  # 这里替换为实际预期的输出


def test_case_1():
    prompt_lib_file = "./backend_server/persona/prompt_template//v3_ChatGPT/generate_obj_event_v1.txt"

    prompt_input = ['bed', 'Isabella Rodriguez', 'sleeping', 'bed', 'bed']
    prompt = generate_prompt(prompt_input, prompt_lib_file)
    example_output = "being fixed"
    special_instruction = "The output should ONLY contain the phrase that should go in <fill in>."

    def __chat_func_clean_up(gpt_response, prompt=""):
        cr = gpt_response.strip()
        if cr[-1] == ".":
            cr = cr[:-1]
        return cr

    def __func_clean_up(gpt_response, prompt):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    def __chat_func_validate(gpt_response, prompt=""):
        try:
            gpt_response = __func_clean_up(gpt_response, prompt="")
        except:
            return False
        return True

    output = ChatGPT_safe_generate_response(
        prompt,
        example_output,
        special_instruction,
        3,
        "None",
        __chat_func_validate,
        __chat_func_clean_up,
        True,
    )
    logger.info(output)

    assert output == "being slept on"  # 这里替换为实际预期的输出

