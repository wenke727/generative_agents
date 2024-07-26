"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: print_prompt.py
Description: For printing prompts when the setting for verbose is set to True.
"""

from loguru import logger


def print_run_prompts(
    prompt_template=None,
    persona=None,
    gpt_param=None,
    prompt_input=None,
    prompt=None,
    output=None,
):
    log_message = f"""
### persona
  {persona.name if persona else "None"}

### prompt_input
  {prompt_input}

### prompt_template:
  {prompt_template}

### Prompt
{prompt}

### Output
{output}
"""
# `gpt_param`: {gpt_param}

    logger.debug(log_message)