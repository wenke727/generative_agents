"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: converse.py
Description: An extra cognitive module for generating conversations.
"""

import sys
import datetime
from loguru import logger

sys.path.append("../")

from persona.cognitive_modules.retrieve import new_retrieve
from persona.prompt_template.gpt_structure import get_embedding
from persona.prompt_template.run_gpt_prompt import (
    run_gpt_generate_iterative_chat_utt,
    run_gpt_generate_safety_score,
    run_gpt_prompt_agent_chat,
    run_gpt_prompt_agent_chat_summarize_ideas,
    run_gpt_prompt_agent_chat_summarize_relationship,
    run_gpt_prompt_chat_poignancy,
    run_gpt_prompt_event_poignancy,
    run_gpt_prompt_event_triple,
    run_gpt_prompt_generate_next_convo_line,
    run_gpt_prompt_generate_whisper_inner_thought,
    run_gpt_prompt_summarize_ideas,
)
from utils import debug


""" decrapted """
def _generate_agent_chat_summarize_ideas(init_persona, target_persona, retrieved, curr_context):
    all_embedding_keys = list()
    for key, val in retrieved.items():
        for i in val:
            all_embedding_keys += [i.embedding_key]
    all_embedding_key_str = ""
    for i in all_embedding_keys:
        all_embedding_key_str += f"{i}\n"

    try:
        summarized_idea = run_gpt_prompt_agent_chat_summarize_ideas(
            init_persona, target_persona, all_embedding_key_str, curr_context)[0]

    except:
        summarized_idea = ""
    return summarized_idea


def _generate_summarize_agent_relationship(init_persona, target_persona, retrieved):
    all_embedding_keys = list()
    for key, val in retrieved.items():
        for i in val:
            all_embedding_keys += [i.embedding_key]
    all_embedding_key_str = ""
    for i in all_embedding_keys:
        all_embedding_key_str += f"{i}\n"

    summarized_relationship = run_gpt_prompt_agent_chat_summarize_relationship(
        init_persona, target_persona, all_embedding_key_str)[0]

    return summarized_relationship


def _generate_agent_chat(
    maze, init_persona, target_persona, curr_context, init_summ_idea, target_summ_idea
):
    summarized_idea = run_gpt_prompt_agent_chat(
        maze,
        init_persona,
        target_persona,
        curr_context,
        init_summ_idea,
        target_summ_idea,
    )[0]
    for i in summarized_idea:
        logger.debug(i)
    return summarized_idea


def _agent_chat_v1(maze, init_persona, target_persona):
    # Chat version optimized for speed via batch generation
    curr_context = (
        f"{init_persona.name} "
        + f"was {init_persona.act_description} "
        + f"when {init_persona.name} "
        + f"saw {target_persona.name} "
        + f"in the middle of {target_persona.act_description}.\n"
    )
    curr_context += (
        f"{init_persona.name} "
        + f"is thinking of initating a conversation with "
        + f"{target_persona.name}."
    )

    summarized_ideas = []
    part_pairs = [(init_persona, target_persona), (target_persona, init_persona)]
    for p_1, p_2 in part_pairs:
        focal_points = [f"{p_2.scratch.name}"]
        retrieved = new_retrieve(p_1, focal_points, 50)
        relationship = _generate_summarize_agent_relationship(p_1, p_2, retrieved)
        focal_points = [
            f"{relationship}",
            f"{p_2.scratch.name} is {p_2.scratch.act_description}",
        ]
        retrieved = new_retrieve(p_1, focal_points, 25)
        summarized_idea = _generate_agent_chat_summarize_ideas(
            p_1, p_2, retrieved, curr_context
        )
        summarized_ideas += [summarized_idea]

    return _generate_agent_chat(
        maze,
        init_persona,
        target_persona,
        curr_context,
        summarized_ideas[0],
        summarized_ideas[1],
    )


""" new """
def _generate_one_utterance(maze, init_persona, target_persona, retrieved, curr_chat):
    # Chat version optimized for speed via batch generation
    curr_context = (
        f"{init_persona.name} "
        + f"was {init_persona.act_description} "
        + f"when {init_persona.name} "
        + f"saw {target_persona.name} "
        + f"in the middle of {target_persona.act_description}.\n"
    )
    curr_context += (
        f"{init_persona.name} "
        + f"is initiating a conversation with "
        + f"{target_persona.name}."
    )

    x = run_gpt_generate_iterative_chat_utt(
        maze, init_persona, target_persona, retrieved, curr_context, curr_chat)[0]

    return x["utterance"], x["end"]


def agent_chat_v2(maze, init_persona, target_persona):
    curr_chat = []

    for i in range(8):
        focal_points = [f"{target_persona.name}"]
        retrieved = new_retrieve(init_persona, focal_points, 50)
        relationship = _generate_summarize_agent_relationship(
            init_persona, target_persona, retrieved
        )
        logger.info(relationship)

        last_chat = ""
        for i in curr_chat[-4:]:
            last_chat += ": ".join(i) + "\n"
        if last_chat:
            focal_points = [
                f"{relationship}",
                f"{target_persona.name} is {target_persona.act_description}",
                last_chat,
            ]
        else:
            focal_points = [
                f"{relationship}",
                f"{target_persona.name} is {target_persona.act_description}",
            ]
        retrieved = new_retrieve(init_persona, focal_points, 15)
        utt, end = _generate_one_utterance(
            maze, init_persona, target_persona, retrieved, curr_chat
        )

        curr_chat += [[init_persona.name, utt]]
        if end:
            break

        focal_points = [f"{init_persona.name}"]
        retrieved = new_retrieve(target_persona, focal_points, 50)
        relationship = _generate_summarize_agent_relationship(
            target_persona, init_persona, retrieved
        )
        logger.info(relationship)

        last_chat = ""
        for i in curr_chat[-4:]:
            last_chat += ": ".join(i) + "\n"
        if last_chat:
            focal_points = [
                f"{relationship}",
                f"{init_persona.name} is {init_persona.act_description}",
                last_chat,
            ]
        else:
            focal_points = [
                f"{relationship}",
                f"{init_persona.name} is {init_persona.act_description}",
            ]
        retrieved = new_retrieve(target_persona, focal_points, 15)
        utt, end = _generate_one_utterance(
            maze, target_persona, init_persona, retrieved, curr_chat
        )

        curr_chat += [[target_persona.name, utt]]
        if end:
            break

    tmp = '\n\t'.join(curr_chat)
    logger.debug(f"curr_chat:\n\t{tmp}")

    return curr_chat


def _generate_summarize_ideas(persona, nodes, question):
    statements = ""
    for n in nodes:
        statements += f"{n.embedding_key}\n"
    summarized_idea = run_gpt_prompt_summarize_ideas(persona, statements, question)[0]
    return summarized_idea


def _generate_next_line(persona, interlocutor_desc, curr_convo, summarized_idea):
    # Original chat -- line by line generation
    prev_convo = ""
    for row in curr_convo:
        prev_convo += f"{row[0]}: {row[1]}\n"

    next_line = run_gpt_prompt_generate_next_convo_line(
        persona, interlocutor_desc, prev_convo, summarized_idea
    )[0]
    return next_line


def _generate_inner_thought(persona, whisper):
    inner_thought = run_gpt_prompt_generate_whisper_inner_thought(persona, whisper)[0]
    return inner_thought


def _generate_action_event_triple(act_desp, persona):
    """TODO

    INPUT:
      act_desp: the description of the action (e.g., "sleeping")
      persona: The Persona class instance
    OUTPUT:
      a string of emoji that translates action description.
    EXAMPLE OUTPUT:
      "🧈🍞"
    """
    return run_gpt_prompt_event_triple(act_desp, persona)[0]


def _generate_poig_score(persona, event_type, description):
    if "is idle" in description:
        return 1

    if event_type == "event" or event_type == "thought":
        return run_gpt_prompt_event_poignancy(persona, description)[0]
    elif event_type == "chat":
        return run_gpt_prompt_chat_poignancy(persona, persona.act_description)[
            0
        ]


def load_history_via_whisper(personas, whispers):
    for count, row in enumerate(whispers):
        persona = personas[row[0]]
        whisper = row[1]

        thought = _generate_inner_thought(persona, whisper)

        created = persona.curr_time
        expiration = persona.curr_time + datetime.timedelta(days=30)
        s, p, o = _generate_action_event_triple(thought, persona)
        keywords = set([s, p, o])
        thought_poignancy = _generate_poig_score(persona, "event", whisper)
        thought_embedding_pair = (thought, get_embedding(thought))
        persona.add_thought(
            created,
            expiration,
            s,
            p,
            o,
            thought,
            keywords,
            thought_poignancy,
            thought_embedding_pair,
            None,
        )


def open_convo_session(persona, convo_mode):
    if convo_mode == "analysis":
        curr_convo = []
        interlocutor_desc = "Interviewer"

        while True:
            line = input("Enter Input: ")
            if line == "end_convo":
                break

            if int(run_gpt_generate_safety_score(persona, line)[0]) >= 8:
                logger.debug(
                    f"{persona.name} is a computational agent, and as such, it may be inappropriate to attribute human agency to the agent in your communication."
                )

            else:
                retrieved = new_retrieve(persona, [line], 50)[line]
                summarized_idea = _generate_summarize_ideas(persona, retrieved, line)
                curr_convo += [[interlocutor_desc, line]]

                next_line = _generate_next_line(
                    persona, interlocutor_desc, curr_convo, summarized_idea
                )
                curr_convo += [[persona.name, next_line]]

    elif convo_mode == "whisper":
        whisper = input("Enter Input: ")
        thought = _generate_inner_thought(persona, whisper)

        created = persona.curr_time
        expiration = persona.curr_time + datetime.timedelta(days=30)
        s, p, o = _generate_action_event_triple(thought, persona)
        keywords = set([s, p, o])
        thought_poignancy = _generate_poig_score(persona, "event", whisper)
        thought_embedding_pair = (thought, get_embedding(thought))
        persona.add_thought(
            created,
            expiration,
            s,
            p,
            o,
            thought,
            keywords,
            thought_poignancy,
            thought_embedding_pair,
            None,
        )
