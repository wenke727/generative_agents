# Plan 模块

## 脚本功能概述

`plan.py` 脚本定义了生成型代理（generative agents）的 "Plan" 模块。该模块负责生成代理的日常计划，包括长短期计划，反应计划，以及与其他代理的互动计划。通过与 GPT-3 模型交互生成代理的每日活动计划，并基于代理的感知和检索到的信息进行相应的反应。

## 1. 核心类和方法

`plan` 函数是生成型代理的规划模块，用于根据感知和记忆信息生成代理角色的日常计划和短期行动计划。以下是函数的详细步骤和调用顺序：

### 主要步骤
1. **长远规划 (Long-Term Planning)**
    - 如果是新的一天，调用 `_long_term_planning` 生成代理角色的每日计划。

2. **确定行动 (Determine Action)**
    - 如果当前行动已经完成，调用 `_determine_action` 生成代理角色的下一个行动。

3. **处理感知事件 (Handle Perceived Events)**
    - 从检索到的记忆中选择一个事件进行关注，并决定是否需要对该事件进行反应。

4. **聊天相关状态清理 (Chat-Related State Cleanup)**
    - 清理聊天相关的状态，确保代理角色不会无限循环地进行对话。

### 函数调用顺序
1. **plan**
    - 调用 `_long_term_planning` 生成长期计划
      - **_generate_wake_up_hour**: 生成角色的起床时间
      - **_generate_first_daily_plan**: 生成角色的第一天的日常计划
      - **_revise_identity**: 获取角色的身份信息， stable identify set
      - **_generate_hourly_schedule**: 生成每小时的计划

    - 调用 `_determine_action` 生成短期行动
      - **_determine_decomp**: 确定是否需要分解任务
      - **_generate_task_decomp**: 任务分解
      - **_generate_action_sector**: 生成行动区域
      - **_generate_action_arena**: 生成行动竞技场
      - **_generate_action_game_object**: 生成行动的游戏对象
      - **_generate_action_pronunciatio**: 生成行动的描述
      - **_generate_action_event_triple**: 生成行动事件三元组
      - **_generate_act_obj_desc**: 生成对象描述
      - **_generate_act_obj_event_triple**: 生成对象事件三元组

    - 调用 `_choose_retrieved` 选择检索到的事件 / 执行过滤条件后，随机挑选

    - 调用 `_should_react` 决定是否需要反应
      - **_lets_talk / _generate_decide_to_talk**: 决定是否进行对话
      - **_lets_react / _generate_decide_to_react**: 决定是否进行反应

    - 如果需要对话，调用 `_chat_react` 生成对话
      - **_generate_convo**: 生成对话
      - **_generate_convo_summary**: 生成对话总结
      - **_create_react**: 创建反应
        - **_generate_new_decomp_schedule**: 生成新的分解计划

    - 如果需要等待，调用 `_wait_react` 进行等待
      - **_create_react**: 创建反应



当然可以。以下是 `plan` 函数的总体逻辑梳理：

## plan 函数总体逻辑

### 输入参数
- `persona`: 当前的 Persona 实例。
- `maze`: 当前的 Maze 实例，表示世界的状态。
- `personas`: 包含所有 Persona 名称作为键和 Persona 实例作为值的字典。
- `new_day`: 表示当前时间是否为新的一天，有三种可能的值：`False`（不是新的一天）、`"First day"`（模拟的第一天）、`"New day"`（新的一天）。
- `retrieved`: 一个字典，包含检索到的事件，形式为 `dictionary[event.description] = {"curr_event": <ConceptNode>, "events": [<ConceptNode>, ...], "thoughts": [<ConceptNode>, ...]}`。

### 输出
- 返回 Persona 的目标行为地址 `persona.scratch.act_address`。

### 函数流程

#### 第一步：生成小时计划（如果是新的一天）
```python
if new_day:
    _long_term_planning(persona, new_day)
```
- 如果是新的一天，调用 `_long_term_planning` 函数生成一天的计划。
  - `_generate_wake_up_hour`：生成起床时间。
  - `_generate_first_daily_plan` 或 `_revise_identity`：生成或修订每日计划。
  - `_generate_hourly_schedule`：生成每小时的计划。

#### 第二步：如果当前行为已结束，创建新计划

```python
if persona.scratch.act_check_finished():
    _determine_action(persona, maze)
```
- 如果当前行为已结束，调用 `_determine_action` 函数创建新的行为序列。
  - `_generate_task_decomp`：任务分解。
  - `_generate_action_sector`：生成行动的区域。
  - `_generate_action_arena`：生成行动的场所。
  - `_generate_action_game_object`：生成行动的游戏对象。
  - `_generate_action_pronunciatio`：生成行动的描述。
  - `_generate_action_event_triple`：生成行动的事件三元组。
  - `_generate_act_obj_desc`：生成对象的描述。
  - `_generate_act_obj_event_triple`：生成对象的事件三元组。

#### 第三步：处理感知到的事件并决定是否需要响应
```python
focused_event = False
if retrieved.keys():
    focused_event = _choose_retrieved(persona, retrieved)
```
- 如果有感知到的事件，选择一个事件进行处理。
  - `_choose_retrieved`：选择一个需要关注的事件。

```python
if focused_event:
    reaction_mode = _should_react(persona, focused_event, personas)
    if reaction_mode:
        if reaction_mode[:9] == "chat with":
            _chat_react(maze, persona, focused_event, reaction_mode, personas)
        elif reaction_mode[:4] == "wait":
            _wait_react(persona, reaction_mode)
```
- 如果选择了一个事件，判断是否需要对该事件做出反应。
  - `_should_react`：确定反应的形式（聊天、等待或不反应）。
    - `_lets_talk`：判断是否需要聊天。
    - `_lets_react`：判断是否需要其他反应。

- 根据反应模式调用相应的函数：
  - `_chat_react`：生成对话并更新行为计划。
  - `_wait_react`：生成等待行为并更新行为计划。

#### 第四步：清理聊天相关状态
```python
if persona.scratch.act_event[1] != "chat with":
    persona.scratch.chatting_with = None
    persona.scratch.chat = None
    persona.scratch.chatting_end_time = None
```
- 如果当前行为不是聊天，清理聊天相关状态。

#### 第五步：维护聊天缓冲机制
```python
curr_persona_chat_buffer = persona.scratch.chatting_with_buffer
for persona_name, buffer_count in curr_persona_chat_buffer.items():
    if persona_name != persona.scratch.chatting_with:
        persona.scratch.chatting_with_buffer[persona_name] -= 1
```
- 维护聊天缓冲机制，确保角色不会立即与同一个目标角色再次进行对话。

### 总结
`plan` 函数是 Persona 的主要认知函数，它结合了长期和短期的计划，通过感知和记忆信息来决定角色的下一步行动，并确保角色之间的互动不会陷入无限循环。



![image-25670730132155618](.fig/Plan.asset/plan.png)


| 函数名                           | 描述                                                         | 输入参数                                                     | 输出                                           |
| -------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------- |
| `_generate_wake_up_hour`         | 生成角色的起床时间                                           | `persona`                                                    | 一个整数，表示角色的起床时间                   |
| `_generate_first_daily_plan`     | 生成角色的每日计划，返回当天的行动列表                       | `persona` ，<br />`wake_up_hour`                             | 一份每日行动列表                               |
| `_generate_hourly_schedule`      | 根据每日计划生成每小时的安排                                 | `persona` ，<br />`wake_up_hour`                             | 一个活动和其持续时间（分钟）列表               |
| `_generate_task_decomp`          | 分解给定的任务                                               | `persona` ，<br />`task` <br />`duration` (整数，任务持续时间) | 一个包含分解任务描述及其持续时间的列表         |
| `_generate_action_sector`        | 生成行动的区域                                               | `act_desp` (字符串，行动描述)，<br />`persona` ，<br />`maze` (Maze 类实例) | 一个字符串，表示行动的区域                     |
| `_generate_action_arena`         | 生成行动的竞技场                                             | `act_desp` (字符串，行动描述)，<br />`persona` ，<br />`maze` (Maze 类实例)，<br />`act_world` (字符串)，<br />`act_sector` (字符串) | 一个字符串，表示行动的竞技场                   |
| `_generate_action_game_object`   | 生成行动的游戏对象                                           | `act_desp` (字符串，行动描述)，<br />`act_address` (字符串，行动地址)，<br />`persona` ，<br />`maze` (Maze 类实例) | 一个字符串，表示行动的游戏对象                 |
| `_generate_action_pronunciatio`  | 生成行动的表情描述                                           | `act_desp` (字符串，行动描述)，<br />`persona`               | 一个字符串，表示行动的表情描述                 |
| `_generate_action_event_triple`  | 生成行动的事件三元组                                         | `act_desp` (字符串，行动描述)，<br />`persona`               | 一个字符串，表示行动的事件三元组               |
| `_generate_act_obj_desc`         | 生成行动对象的描述                                           | `act_game_object` (字符串)，<br />`act_desp` (字符串)，<br />`persona` | 一个字符串，表示行动对象的描述                 |
| `_generate_act_obj_event_triple` | 生成行动对象的事件三元组                                     | `act_game_object` (字符串)，<br />`act_obj_desc` (字符串)，<br />`persona` | 一个字符串，表示行动对象的事件三元组           |
| `_generate_convo`                | 生成对话                                                     | `maze` (Maze 类实例)，<br />`init_persona` ，<br />`target_persona` | 对话内容和对话长度                             |
| `_generate_convo_summary`        | 生成对话总结                                                 | `persona` ，<br />`convo` (对话内容)                         | 一个字符串，表示对话总结                       |
| `_generate_decide_to_talk`       | 决定是否进行对话                                             | `init_persona` ，<br />`target_persona` ，<br />`retrieved` (字典) | 一个布尔值，表示是否进行对话                   |
| `_generate_decide_to_react`      | 决定是否做出反应                                             | `init_persona` ，<br />`target_persona` ，<br />`retrieved` (字典) | 一个字符串，表示反应模式                       |
| `generate_new_decomp_schedule`   | 生成新的分解日程                                             | `persona` ，<br />`inserted_act` (字符串)，<br />`inserted_act_dur` (整数)，<br />`start_hour` (整数)，<br />`end_hour` (整数) | 一个新的日程列表                               |
| `_revise_identity`               | 修改角色的身份信息                                           | `persona`                                                    | 无                                             |
| `_long_term_planning`            | 制定角色的长期计划，如果是新的一天，则生成起床时间和小时计划 | `persona` ，<br />`new_day` (布尔值或字符串)                 | 无                                             |
| `_determine_action`              | 创建角色的下一个行动序列，并设置所有相关的行动变量           | `persona` ，<br />`maze` (Maze 类实例)                       | 无                                             |
| `_choose_retrieved`              | 从检索到的记忆中选择一个事件以进行反应                       | `persona` ，<br />`retrieved` (字典)                         | 一个字典，表示选择的事件                       |
| `_should_react`                  | 确定角色在给定的检索值下应如何反应                           | `persona` ，<br />`retrieved` (字典)，<br />`personas` (字典) | 一个字符串，表示反应模式，或者布尔值表示不反应 |
| `_create_react`                  | 创建新的反应并添加到角色的行动队列中                         | `persona` ，<br />`inserted_act` (字符串)，<br />`inserted_act_dur` (整数)，<br />`act_address` (字符串)，<br />`act_event` (元组)，<br />`chatting_with` (字符串)，<br />`chat` (对话内容)，<br />`chatting_with_buffer` (字典)，<br />`chatting_end_time` (时间)，<br />`act_pronunciatio` (字符串)，<br />`act_obj_description` (字符串)，<br />`act_obj_pronunciatio` (字符串)，<br />`act_obj_event` (元组)，<br />`act_start_time` (时间) | 无                                             |
| `_chat_react`                    | 处理聊天反应，并调用之前定义的函数生成对话和添加反应         | `maze` (Maze 类实例)，<br />`persona` ，<br />`focused_event` (字典)，<br />`reaction_mode` (字符串)，<br />`personas` (字典) | 无                                             |
| `_wait_react`                    | 处理等待反应，并调用之前定义的函数生成等待的反应             | `persona` ，<br />`reaction_mode` (字符串)                   | 无                                             |
| `plan`                           | 主要的认知函数，用于根据检索到的记忆和感知、迷宫以及初始状态来进行长期和短期的计划 | `persona` ，<br />`maze` (Maze 类实例)，<br />`personas` (字典)，<br />`new_day` (布尔值或字符串)，<br />`retrieved` (字典) | 一个字符串，表示目标行动地址                   |

## 4. 总结

`plan.py` 脚本定义了生成型代理的计划模块，通过生成每日活动计划和反应计划，使代理能够在虚拟世界中智能地进行长短期决策和行动。该模块与 GPT-3 模型交互生成计划，并根据代理的感知和检索信息调整计划，从而提升代理的智能性和适应性。

