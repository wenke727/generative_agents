"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
import sys
sys.path.append("../../")

import json
import time
import openai
from loguru import logger

from persona.prompt_template.openai_helper import initialize_openai_client, GPT_35_TURBO


client, chat, embeddings = initialize_openai_client()


def _temp_sleep(seconds=0.15):
    time.sleep(seconds)


def ChatGPT_single_request(prompt):
    _temp_sleep()

    completion = chat(
        model=GPT_35_TURBO, messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]


""" SECTION 1: CHATGPT-3 STRUCTURE """
def _GPT4_request(prompt):
    """
    Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
    server and returns the response.
    ARGS:
      prompt: a str prompt
      gpt_parameter: a python dictionary with the keys indicating the names of
                     the parameter and the values indicating the parameter
                     values.
    RETURNS:
      a str of GPT-3's response.
    """
    _temp_sleep()

    try:
        completion = chat(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return completion["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "ChatGPT ERROR"


def _ChatGPT_request(prompt):
    """
    Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
    server and returns the response.
    ARGS:
      prompt: a str prompt
      gpt_parameter: a python dictionary with the keys indicating the names of
                     the parameter and the values indicating the parameter
                     values.
    RETURNS:
      a str of GPT-3's response.
    """
    # temp_sleep()
    try:
        completion = chat(
            model=GPT_35_TURBO, messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
        # return completion["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "ChatGPT ERROR"


def _GPT4_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
    prompt += (
        f"Output the response to the prompt above in json. {special_instruction}\n"
    )
    prompt += "Example output json:\n"
    prompt += '{"output": "' + str(example_output) + '"}'

    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat):

        try:
            curr_gpt_response = _GPT4_request(prompt).strip()
            end_index = curr_gpt_response.rfind("}") + 1
            curr_gpt_response = curr_gpt_response[:end_index]
            curr_gpt_response = json.loads(curr_gpt_response)["output"]

            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)

            if verbose:
                print("---- repeat count: \n", i, curr_gpt_response)
                print(curr_gpt_response)
                print("~~~~")

        except:
            pass

    return False


def ChatGPT_safe_generate_response(
    prompt,
    example_output,
    special_instruction,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    # prompt = '"""\n' + prompt + '\n"""\n'
    # prompt += (
    #     f"Output the response to the prompt above in json. {special_instruction}\n"
    # )
    # prompt += "Example output json:\n"
    # prompt += '{"output": "' + str(example_output) + '"}'

    prompt = f'''{prompt}
----
Output the response to the prompt above in json. {special_instruction}
Example output json:
{{"output": "{str(example_output)}"}}
'''

    for i in range(repeat):
        try:
            curr_gpt_response = _ChatGPT_request(prompt).strip()
            end_index = curr_gpt_response.rfind("}") + 1
            curr_gpt_response = curr_gpt_response[:end_index]
            curr_gpt_response = json.loads(curr_gpt_response)["output"]

            # print ("---ashdfaf")
            # print (curr_gpt_response)
            # print ("000asdfhia")

            if verbose:
                # print("---- repeat count: \n", i, curr_gpt_response)
                logger.debug(f"prompt : {prompt}, \ngpt_response: {curr_gpt_response}")
                # print(curr_gpt_response)
                # print("~~~~")

            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)

        except:
            pass

    return False


def ChatGPT_safe_generate_response_OLD(
    prompt,
    repeat=3,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        print("CHAT GPT PROMPT")
        print(prompt)

    for i in range(repeat):
        try:
            curr_gpt_response = _ChatGPT_request(prompt).strip()
            if func_validate(curr_gpt_response, prompt=prompt):
                return func_clean_up(curr_gpt_response, prompt=prompt)
            if verbose:
                print(f"---- repeat count: {i}")
                print(curr_gpt_response)
                print("~~~~")

        except:
            pass
    print("FAIL SAFE TRIGGERED")
    return fail_safe_response


""" SECTION 2: ORIGINAL GPT-3 STRUCTURE """
def _GPT_request(prompt, gpt_parameter):
    """
    Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
    server and returns the response.
    ARGS:
      prompt: a str prompt
      gpt_parameter: a python dictionary with the keys indicating the names of
                     the parameter and the values indicating the parameter
                     values.
    RETURNS:
      a str of GPT-3's response.
    """
    _temp_sleep()
    # try:
    response = chat(
        model=gpt_parameter["engine"],
        messages=[{"role": "user", "content": prompt}],
        temperature=gpt_parameter["temperature"],
        max_tokens=gpt_parameter["max_tokens"],
        top_p=gpt_parameter["top_p"],
        frequency_penalty=gpt_parameter["frequency_penalty"],
        presence_penalty=gpt_parameter["presence_penalty"],
        stream=gpt_parameter["stream"],
        stop=gpt_parameter["stop"],
    )
    return response.choices[0].message.content
    # except:
    #     print("TOKEN LIMIT EXCEEDED")
    #     return "TOKEN LIMIT EXCEEDED"


def generate_prompt(curr_input, prompt_lib_file):
    """
    Takes in the current input (e.g. comment that you want to classifiy) and
    the path to a prompt file. The prompt file contains the raw str prompt that
    will be used, which contains the following substr: !<INPUT>! -- this
    function replaces this substr with the actual curr_input to produce the
    final promopt that will be sent to the GPT3 server.
    ARGS:
      curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                  INPUT, THIS CAN BE A LIST.)
      prompt_lib_file: the path to the promopt file.
    RETURNS:
      a str prompt that will be sent to OpenAI's GPT server.
    """
    if type(curr_input) == type("string"):
        curr_input = [curr_input]
    curr_input = [str(i) for i in curr_input]

    f = open(prompt_lib_file, "r")
    prompt = f.read()
    f.close()
    for count, i in enumerate(curr_input):
        prompt = prompt.replace(f"!<INPUT {count}>!", i)
    if "<commentblockmarker>###</commentblockmarker>" in prompt:
        prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
    return prompt.strip()


def safe_generate_response(
    prompt,
    gpt_parameter,
    repeat=5,
    fail_safe_response="error",
    func_validate=None,
    func_clean_up=None,
    verbose=False,
):
    if verbose:
        logger.debug(f"prompt: {prompt}")

    for i in range(repeat):
        curr_gpt_response = _GPT_request(prompt, gpt_parameter)
        if func_validate(curr_gpt_response, prompt=prompt):
            return func_clean_up(curr_gpt_response, prompt=prompt)
        if verbose:
            # print("---- repeat count: ", i, curr_gpt_response)
            logger.info(f"curr_gpt_response: \n{curr_gpt_response}")
            # print("~~~~")
    return fail_safe_response


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    if not text:
        text = "this is blank"
    return embeddings(input=[text], model=model).data[0].embedding


""" SECTION 3: test case """
def _test_case_0():
    gpt_parameter = {
        "engine": GPT_35_TURBO,
        "max_tokens": 50,
        "temperature": 0,
        "top_p": 1,
        "stream": False,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ['"'],
    }
    curr_input = ["driving to a friend's house"]
    prompt_lib_file = "./prompt_template/test_prompt_July5.txt"
    prompt_lib_file = "./v1/test_prompt_July5.txt"
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
        prompt, gpt_parameter, 5, "rest", __func_validate, __func_clean_up, True
    )
    logger.info(output)


def _test_case_1():
    prompt_lib_file = "./v3_ChatGPT/generate_obj_event_v1.txt"

    prompt_input = ['bed', 'Isabella Rodriguez', 'sleeping', 'bed', 'bed']
    prompt = generate_prompt(prompt_input, (prompt_lib_file))
    example_output = "being fixed"  ########
    special_instruction = "The output should ONLY contain the phrase that should go in <fill in>."  ########

    def get_fail_safe(act_game_object):
        fs = f"{act_game_object} is idle"
        return fs

    # ChatGPT Plugin ===========================================================
    def __chat_func_clean_up(gpt_response, prompt=""):  ############
        cr = gpt_response.strip()
        if cr[-1] == ".":
            cr = cr[:-1]
        return cr

    def __func_clean_up(gpt_response, prompt):
        cleaned_response = gpt_response.strip()
        return cleaned_response

    def __chat_func_validate(gpt_response, prompt=""):  ############
        try:
            gpt_response = __func_clean_up(gpt_response, prompt="")
        except:
            return False
        return True


    # fail_safe = get_fail_safe(act_game_object)  ########
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


if __name__ == "__main__":
    _test_case_0()
    _test_case_1()
