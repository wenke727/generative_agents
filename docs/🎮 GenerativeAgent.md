# Generative Agent

## 1. Persona

**Persona**

> `Persona` 类定义了在 Reverie 中为代理人提供动力的基本行为和认知功能。这个类主要包括处理代理人记忆、感知、计划、执行和反思的功能模块。通过与各种记忆结构和认知模块的交互，`Persona` 类能够模拟一个代理人的日常行为和决策过程。

| 函数名称             | 作用                                           | 输入参数                                                     | 输出参数                                                     |
| -------------------- | ---------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `__init__`           | 初始化代理人的基本状态和记忆结构               | `name`: 代理人的名字<br>`folder_mem_saved`: 存储记忆的文件夹路径 | 无                                                           |
| `save`               | 保存代理人的当前状态（记忆）                   | `save_folder`: 保存代理人状态的文件夹路径                    | 无                                                           |
| `perceive`           | 感知当前迷宫中的事件，返回代理人周围发生的事件 | `maze`: 当前世界的迷宫实例                                   | 一个包含新感知到的 <ConceptNode> 列表                        |
| `retrieve`           | 从记忆中检索与感知事件相关的事件和想法         | `perceived`: 一个包含新感知到的 <ConceptNode> 列表           | 一个字典，包含相关的事件和想法                               |
| `plan`               | 进行代理人的长期和短期计划                     | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`new_day`: 这可以取三个值之一<br>&nbsp;&nbsp;&nbsp;&nbsp;1) <Boolean> False - 不是“新的一天”周期<br>&nbsp;&nbsp;&nbsp;&nbsp;2) <String> "First day" - 实际上是模拟的开始，所以不仅是新的一天，也是第一天<br>&nbsp;&nbsp;&nbsp;&nbsp;3) <String> "New day" - 是新的一天。<br>`retrieved`: 包含相关事件和想法的字典 | 代理人的目标动作地址（`persona.scratch.act_address`）        |
| `execute`            | 执行当前计划，输出具体的执行步骤               | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`plan`: 代理人的目标动作地（`persona.scratch.act_address`） | 一个三元组，包含以下组件：<br>`next_tile`: x,y 坐标<br>`pronunciatio`: 表情符号<br>`description`: 动作描述 |
| `reflect`            | 回顾代理人的记忆，并基于记忆创建新的想法       | 无                                                           | 无                                                           |
| `move`               | 代理人的主要认知函数，调用主要的认知序列       | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`curr_tile`: 当前的x,y坐标<br>`curr_time`: 当前时间实例 | 一个三元组，包含以下组件：<br>`next_tile`: x,y 坐标<br>`pronunciatio`: 表情符号<br>`description`: 动作描述 |
| `open_convo_session` | 打开对话会话                                   | `convo_mode`: 对话模式                                       | 无                                                           |

### Detailed Docstrings for Each Function

1. **`__init__`**
   - **作用**: 初始化代理人的基本状态和记忆结构
   - **输入参数**: 
     - `name`: 代理人的名字
     - `folder_mem_saved`: 存储记忆的文件夹路径
   - **输出参数**: 无

2. **`save`**
   - **作用**: 保存代理人的当前状态（记忆）
   - **输入参数**:
     - `save_folder`: 保存代理人状态的文件夹路径
   - **输出参数**: 无

3. **`perceive`**
   - **作用**: 感知当前迷宫中的事件，返回代理人周围发生的事件
   - **输入参数**:
     - `maze`: 当前世界的迷宫实例
   - **输出参数**: 一个包含新感知到的 <ConceptNode> 列表
   - **详细描述**:
     - 这个函数获取当前迷宫，并返回代理人周围发生的事件。重要的是，感知由代理人的两个关键超参数指导：1）att_bandwidth 和 2）retention。
     - 首先，<att_bandwidth> 确定代理人可以感知的附近事件的数量。假设有10个事件在代理人的视野范围内——感知所有10个可能太多。因此，代理人在事件过多的情况下，会感知最近的 att_bandwidth 数量的事件。
     - 其次，代理人不希望在每个时间步都感知并思考同一个事件。这就是 <retention> 的作用——代理人的记忆有时间顺序。所以如果代理人的记忆中包含最近 retention 发生的当前周围事件，就不需要再次感知这些事件。

4. **`retrieve`**
   - **作用**: 从记忆中检索与感知事件相关的事件和想法
   - **输入参数**:
     - `perceived`: 一个包含新感知到的 <ConceptNode> 列表
   - **输出参数**: 一个字典，包含相关的事件和想法

5. **`plan`**
   - **作用**: 进行代理人的长期和短期计划
   - **输入参数**:
     - `maze`: 当前世界的迷宫实例
     - `personas`: 包含所有代理人的字典
     - `new_day`: 这可以取三个值之一:
       1) <Boolean> False - 不是“新的一天”周期（如果是，我们需要调用代理人的长期计划序列）
       2) <String> "First day" - 实际上是模拟的开始，所以不仅是新的一天，也是第一天
       3) <String> "New day" - 是新的一天
     - `retrieved`: 包含相关事件和想法的字典
   - **输出参数**: 代理人的目标动作地址（`persona.scratch.act_address`）

6. **`execute`**
   - **作用**: 执行当前计划，输出具体的执行步骤
   - **输入参数**:
     - `maze`: 当前世界的迷宫实例
     - `personas`: 包含所有代理人的字典
     - `plan`: 代理人的目标动作地址（`persona.scratch.act_address`）
   - **输出参数**: 一个三元组，包含以下组件：
     - `next_tile`: x,y 坐标
     - `pronunciatio`: 表情符号
     - `description`: 动作描述

7. **`reflect`**
   - **作用**: 回顾代理人的记忆，并基于记忆创建新的想法
   - **输入参数**: 无
   - **输出参数**: 无

8. **`move`**
   - **作用**: 代理人的主要认知函数，调用主要的认知序列
   - **输入参数**:
     - `maze`: 当前世界的迷宫实例
     - `personas`: 包含所有代理人的字典
     - `curr_tile`: 当前的x,y坐标
     - `curr_time`: 当前时间实例
   - **输出参数**: 一个三元组，包含以下组件：
     - `next_tile`: x,y 坐标
     - `pronunciatio`: 表情符号
     - `description`: 动作描述

9. **`open_convo_session`**
   - **作用**: 打开对话会话
   - **输入参数**:
     - `convo_mode`: 对话模式
   - **输出参数**: 无

这样你就可以使用新的模型来生成所需的内容。你可以使用 OpenAI 的 Python SDK 调用 `gpt-4` 模型来完成此任务。

## 2. cognitive_modules

### 2.1 converse

`converse.py`脚本的主要作用是定义和实现生成性代理（generative agents）之间的对话模块。它包含多个函数，这些函数协同工作，以生成和管理代理之间的对话内容。具体来说，它的功能包括：

1. **生成聊天总结**：提取和总结两个代理之间的聊天内容和关系。
2. **生成代理聊天**：根据特定情境和角色设定，生成代理之间的对话内容。
3. **管理对话流程**：包括初始化对话、生成单句对话、总结对话等。
4. **生成内部思维和行动描述**：生成代理的内部思维（内心独白）和行动描述，增强对话的真实性和连贯性。
5. **评估事件影响力**：对生成的事件进行评分，以确定其对话或事件的影响力。

通过这些功能，`converse.py`实现了一个复杂的对话生成系统，使得生成性代理能够进行有逻辑和上下文关联的对话。

| 函数名称                                | 作用                     | 输入                                                                                           | 输出                      |
| --------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------- |
| `generate_agent_chat_summarize_ideas`   | 生成代理聊天总结想法     | `init_persona`, `target_persona`, `retrieved`, `curr_context`                                  | `summarized_idea`         |
| `generate_summarize_agent_relationship` | 生成代理关系总结         | `init_persona`, `target_persona`, `retrieved`                                                  | `summarized_relationship` |
| `generate_agent_chat`                   | 生成代理聊天             | `maze`, `init_persona`, `target_persona`, `curr_context`, `init_summ_idea`, `target_summ_idea` | `summarized_idea`         |
| `agent_chat_v1`                         | 优化批量生成的聊天版本 1 | `maze`, `init_persona`, `target_persona`                                                       | 生成的聊天内容            |
| `generate_one_utterance`                | 生成单句对话             | `maze`, `init_persona`, `target_persona`, `retrieved`, `curr_chat`                             | `utterance`, `end`        |
| `agent_chat_v2`                         | 优化批量生成的聊天版本 2 | `maze`, `init_persona`, `target_persona`                                                       | 生成的聊天内容            |
| `generate_summarize_ideas`              | 生成总结想法             | `persona`, `nodes`, `question`                                                                 | `summarized_idea`         |
| `generate_next_line`                    | 生成下一行对话           | `persona`, `interlocutor_desc`, `curr_convo`, `summarized_idea`                                | `next_line`               |
| `generate_inner_thought`                | 生成内心想法             | `persona`, `whisper`                                                                           | `inner_thought`           |
| `generate_action_event_triple`          | 生成动作事件三元组       | `act_desp`, `persona`                                                                          | 动作描述的字符串          |
| `generate_poig_score`                   | 生成事件的影响力评分     | `persona`, `event_type`, `description`                                                         | `poig_score`              |
| `load_history_via_whisper`              | 通过私语加载历史记录     | `personas`, `whispers`                                                                         | 无返回值                  |
| `open_convo_session`                    | 打开对话会话             | `persona`, `convo_mode`                                                                        | 无返回值                  |

### 2.2 execute

| 函数名称  | 作用                                                   | 输入                                  | 输出                                          |
| --------- | ------------------------------------------------------ | ------------------------------------- | --------------------------------------------- |
| `execute` | 根据给定的计划执行动作，输出角色的路径坐标和下一个坐标 | `persona`, `maze`, `personas`, `plan` | `execution`（包含下一个坐标、动作发音、描述） |

### 2.3 plan

`plan.py`脚本的主要作用是定义生成性代理（generative agents）的"计划"模块。这个模块负责生成和管理代理的日常活动计划，包括长期计划和短期计划。具体来说，它的功能包括：

1. **生成日常计划**：

   - 确定代理的起床时间。
   - 生成代理的一天中要进行的主要活动列表。
   - 将这些活动细化为每小时的计划。

2. **任务分解**：

   - 将复杂的任务分解为更小的可执行步骤。
   - 确定每个任务的具体执行时间和地点。

3. **生成行动细节**：

   - 选择行动的具体区域、场所和对象。
   - 生成行动的描述、发音和事件三元组（表示行动的具体细节）。

4. **对话生成**：

   - 根据当前情境生成代理之间的对话。
   - 总结对话内容并决定代理是否进行对话或反应。

5. **反应管理**：

   - 评估代理是否需要对环境中的事件进行反应。
   - 根据评估结果生成具体的反应行动，如对话、等待等。

6. **长期计划和短期计划**：
   - 在新的一天开始时，生成代理的长期计划和每天的详细活动安排。
   - 如果当前行动已完成，则生成新的行动计划。

通过这些功能，`plan.py`脚本为生成性代理提供了一个完整的计划和行动框架，使代理能够根据预定的计划和实时的环境变化进行合理的行动和互动。

| 函数名称                        | 作用                           | 输入                                                                                                                                                                                                                                                  | 输出                                                      |
| ------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `generate_wake_up_hour`         | 生成代理的起床时间             | `persona`                                                                                                                                                                                                                                             | `wake_up_hour`（整数，表示起床时间）                      |
| `generate_first_daily_plan`     | 生成代理的日常计划             | `persona`, `wake_up_hour`                                                                                                                                                                                                                             | `daily_plan`（列表，表示每日行动）                        |
| `generate_hourly_schedule`      | 生成每小时的日程安排           | `persona`, `wake_up_hour`                                                                                                                                                                                                                             | `hourly_schedule`（列表，表示每小时的活动和持续时间）     |
| `generate_task_decomp`          | 生成任务分解                   | `persona`, `task`, `duration`                                                                                                                                                                                                                         | `task_decomp`（列表，表示分解后的任务和持续时间）         |
| `generate_action_sector`        | 生成行动区域                   | `act_desp`, `persona`, `maze`                                                                                                                                                                                                                         | `action_sector`（字符串，表示行动区域）                   |
| `generate_action_arena`         | 生成行动场所                   | `act_desp`, `persona`, `maze`, `act_world`, `act_sector`                                                                                                                                                                                              | `action_arena`（字符串，表示行动场所）                    |
| `generate_action_game_object`   | 生成行动对象                   | `act_desp`, `act_address`, `persona`, `maze`                                                                                                                                                                                                          | `act_game_object`（字符串，表示行动对象）                 |
| `generate_action_pronunciatio`  | 生成行动发音                   | `act_desp`, `persona`                                                                                                                                                                                                                                 | `action_pronunciatio`（字符串，表示行动的发音或表情符号） |
| `generate_action_event_triple`  | 生成行动事件三元组             | `act_desp`, `persona`                                                                                                                                                                                                                                 | `action_event_triple`（字符串，表示行动事件三元组）       |
| `generate_act_obj_desc`         | 生成行动对象描述               | `act_game_object`, `act_desp`, `persona`                                                                                                                                                                                                              | `act_obj_desc`（字符串，表示行动对象的描述）              |
| `generate_act_obj_event_triple` | 生成行动对象事件三元组         | `act_game_object`, `act_obj_desc`, `persona`                                                                                                                                                                                                          | `act_obj_event_triple`（字符串，表示行动对象事件三元组）  |
| `generate_convo`                | 生成对话                       | `maze`, `init_persona`, `target_persona`                                                                                                                                                                                                              | `convo`, `convo_length`（生成的对话及其长度）             |
| `generate_convo_summary`        | 生成对话总结                   | `persona`, `convo`                                                                                                                                                                                                                                    | `convo_summary`（字符串，表示对话总结）                   |
| `generate_decide_to_talk`       | 决定是否进行对话               | `init_persona`, `target_persona`, `retrieved`                                                                                                                                                                                                         | `True` 或 `False`（布尔值，表示是否进行对话）             |
| `generate_decide_to_react`      | 决定是否进行反应               | `init_persona`, `target_persona`, `retrieved`                                                                                                                                                                                                         | `reaction_mode`（字符串，表示反应模式）                   |
| `generate_new_decomp_schedule`  | 生成新的分解日程               | `persona`, `inserted_act`, `inserted_act_dur`, `start_hour`, `end_hour`                                                                                                                                                                               | `new_decomp_schedule`（列表，表示新的分解日程）           |
| `revise_identity`               | 修订身份                       | `persona`                                                                                                                                                                                                                                             | 无返回值                                                  |
| `_long_term_planning`           | 长期计划                       | `persona`, `new_day`                                                                                                                                                                                                                                  | 无返回值                                                  |
| `_determine_action`             | 确定行动                       | `persona`, `maze`                                                                                                                                                                                                                                     | 无返回值                                                  |
| `_choose_retrieved`             | 选择检索到的事件               | `persona`, `retrieved`                                                                                                                                                                                                                                | `priority`（字典，表示优先选择的事件）                    |
| `_should_react`                 | 确定是否反应                   | `persona`, `retrieved`, `personas`                                                                                                                                                                                                                    | `reaction_mode`（字符串，表示反应模式）                   |
| `_create_react`                 | 创建反应                       | `persona`, `inserted_act`, `inserted_act_dur`, `act_address`, `act_event`, `chatting_with`, `chat`, `chatting_with_buffer`, `chatting_end_time`, `act_pronunciatio`, `act_obj_description`, `act_obj_pronunciatio`, `act_obj_event`, `act_start_time` | 无返回值                                                  |
| `_chat_react`                   | 处理聊天反应                   | `maze`, `persona`, `focused_event`, `reaction_mode`, `personas`                                                                                                                                                                                       | 无返回值                                                  |
| `_wait_react`                   | 处理等待反应                   | `persona`, `reaction_mode`                                                                                                                                                                                                                            | 无返回值                                                  |
| `plan`                          | 主要的计划函数，进行长短期计划 | `persona`, `maze`, `personas`, `new_day`, `retrieved`                                                                                                                                                                                                 | `act_address`（字符串，表示代理的目标行动地址）           |

### 2.4 reflect

`reflect.py`脚本的主要作用是定义生成性代理（generative agents）的“反思”模块。这个模块负责生成和管理代理的反思过程，通过检索记忆和生成新的想法来更新代理的内部状态。具体来说，它的功能包括：

1. **生成焦点点**：

   - 从代理的记忆中选择重要事件或想法，生成反思的焦点点。

2. **生成见解和证据**：

   - 根据焦点点检索相关的记忆节点，生成新的见解，并提供支持这些见解的证据。

3. **生成行动事件三元组和影响评分**：

   - 对代理的行动进行描述，生成相应的事件三元组和影响评分，以衡量这些事件对代理的重要性。

4. **对话后的反思**：

   - 在对话结束后，生成关于对话的计划性想法和备忘录，并将这些新生成的想法存储在代理的记忆中。

5. **触发反思的条件**：

   - 检查是否满足触发反思的条件，如重要性触发器的当前值是否达到阈值。

6. **运行反思过程**：
   - 如果触发条件满足，执行反思过程，生成新的想法并重置相关计数器。

通过这些功能，`reflect.py`脚本为生成性代理提供了一个全面的反思框架，使代理能够根据过去的经验和当前的情境生成新的想法和见解，从而不断更新和改进自身的行为和计划。

| 函数名称                             | 作用                                   | 输入                                   | 输出                                                 |
| ------------------------------------ | -------------------------------------- | -------------------------------------- | ---------------------------------------------------- |
| `generate_focal_points`              | 生成反思的焦点点                       | `persona`, `n=3`                       | `focal_points`（焦点点）                             |
| `generate_insights_and_evidence`     | 生成见解和支持证据                     | `persona`, `nodes`, `n=5`              | `insights_and_evidence`（字典，见解及其证据节点 ID） |
| `generate_action_event_triple`       | 生成行动事件三元组                     | `act_desp`, `persona`                  | `action_event_triple`（字符串，表示行动事件三元组）  |
| `generate_poig_score`                | 生成事件的影响评分                     | `persona`, `event_type`, `description` | `poig_score`（整数，表示影响评分）                   |
| `generate_planning_thought_on_convo` | 生成关于对话的计划性想法               | `persona`, `all_utt`                   | `planning_thought`（字符串，计划性想法）             |
| `generate_memo_on_convo`             | 生成关于对话的备忘录                   | `persona`, `all_utt`                   | `memo_thought`（字符串，备忘录）                     |
| `run_reflect`                        | 执行反思过程，生成新的想法和见解       | `persona`                              | 无返回值                                             |
| `reflection_trigger`                 | 判断是否触发反思                       | `persona`                              | `True` 或 `False`（布尔值，是否触发反思）            |
| `reset_reflection_counter`           | 重置反思触发计数器                     | `persona`                              | 无返回值                                             |
| `reflect`                            | 主要的反思模块，检查触发条件并执行反思 | `persona`                              | 无返回值                                             |

### 2.5 retrieve

`retrieve.py`脚本的主要作用是定义生成性代理（generative agents）的“检索”模块。这个模块负责从代理的记忆中检索与当前感知事件相关的信息，以帮助代理在规划和决策过程中利用这些信息。具体来说，它的功能包括：

1. **事件和想法的检索**：

   - 根据代理当前感知到的事件，从其记忆中检索相关的事件和想法。

2. **相似度计算**：

   - 计算向量之间的余弦相似度，用于评估记忆节点与当前焦点点的相关性。

3. **评分和归一化**：

   - 计算记忆节点的最近访问时间评分、重要性评分和相关性评分，并将这些评分归一化到指定范围。

4. **筛选和排序**：

   - 根据评分筛选和排序记忆节点，提取前 x 个相关性最高的节点。

5. **焦点点的检索**：
   - 生成当前的焦点点，检索与这些焦点点相关的记忆节点，并更新这些节点的最近访问时间。

通过这些功能，`retrieve.py`脚本为生成性代理提供了一个完整的记忆检索框架，使代理能够根据当前的感知和焦点点从记忆中提取相关信息，从而在规划和决策过程中利用这些信息。

| 函数名称                | 作用                               | 输入                                    | 输出                                                   |
| ----------------------- | ---------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| `retrieve`              | 根据感知的事件检索相关的事件和想法 | `persona`, `perceived`                  | `retrieved`（字典，包含当前事件及其相关的事件和想法）  |
| `cos_sim`               | 计算两个向量之间的余弦相似度       | `a`, `b`                                | `cosine_similarity`（浮点数，表示余弦相似度）          |
| `normalize_dict_floats` | 将字典的浮点值归一化到目标范围     | `d`, `target_min`, `target_max`         | `normalized_dict`（字典，包含归一化后的值）            |
| `top_highest_x_values`  | 获取字典中前 x 个最高值的键值对    | `d`, `x`                                | `top_values`（字典，包含前 x 个最高值的键值对）        |
| `extract_recency`       | 计算节点的最近访问时间评分         | `persona`, `nodes`                      | `recency_scores`（字典，节点 ID 及其最近访问时间评分） |
| `extract_importance`    | 计算节点的重要性评分               | `persona`, `nodes`                      | `importance_scores`（字典，节点 ID 及其重要性评分）    |
| `extract_relevance`     | 计算节点与焦点点的相关性评分       | `persona`, `nodes`, `focal_pt`          | `relevance_scores`（字典，节点 ID 及其相关性评分）     |
| `new_retrieve`          | 根据焦点点检索相关的节点           | `persona`, `focal_points`, `n_count=30` | `retrieved`（字典，焦点点及其相关的节点列表）          |

## 3. memory_structures

### 3.1. associative_memory

**ConceptNode**

> `ConceptNode`类定义了记忆中每个概念节点的结构和属性。每个节点代表代理的一个具体记忆片段，包括事件、想法或聊天内容。这个类主要用于存储和管理这些记忆片段的详细信息。

| 函数名称      | 作用                     | 输入                                                                                                                                                                    | 输出                          |
| ------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `__init__`    | 初始化概念节点对象       | `node_id`, `node_count`, `type_count`, `node_type`, `depth`, `created`, `expiration`, `s`, `p`, `o`, `description`, `embedding_key`, `poignancy`, `keywords`, `filling` | 无                            |
| `spo_summary` | 返回概念节点的主谓宾摘要 | 无                                                                                                                                                                      | `summary`（元组，包含主谓宾） |

**AssociativeMemory**

> `AssociativeMemory`类实现了代理的联想记忆系统，用于存储、管理和检索代理的长期记忆。这些记忆包括事件、想法和聊天内容。该类提供了丰富的方法来处理和操作这些记忆片段，支持代理在生成对话和行为时使用这些记忆。

| 函数名称                       | 作用                         | 输入                                                                                                        | 输出                                  |
| ------------------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `__init__`                     | 初始化联想记忆对象           | `f_saved`                                                                                                   | 无                                    |
| `save`                         | 保存记忆数据到 JSON 文件     | `out_json`                                                                                                  | 无                                    |
| `add_event`                    | 添加事件节点                 | `created`, `expiration`, `s`, `p`, `o`, `description`, `keywords`, `poignancy`, `embedding_pair`, `filling` | `node`（添加的事件节点）              |
| `add_thought`                  | 添加想法节点                 | `created`, `expiration`, `s`, `p`, `o`, `description`, `keywords`, `poignancy`, `embedding_pair`, `filling` | `node`（添加的想法节点）              |
| `add_chat`                     | 添加聊天节点                 | `created`, `expiration`, `s`, `p`, `o`, `description`, `keywords`, `poignancy`, `embedding_pair`, `filling` | `node`（添加的聊天节点）              |
| `get_summarized_latest_events` | 获取最新事件的摘要           | `retention`                                                                                                 | `ret_set`（集合，包含最新事件的摘要） |
| `get_str_seq_events`           | 获取事件序列的字符串表示     | 无                                                                                                          | `ret_str`（字符串，包含事件序列）     |
| `get_str_seq_thoughts`         | 获取想法序列的字符串表示     | 无                                                                                                          | `ret_str`（字符串，包含想法序列）     |
| `get_str_seq_chats`            | 获取聊天序列的字符串表示     | 无                                                                                                          | `ret_str`（字符串，包含聊天序列）     |
| `retrieve_relevant_thoughts`   | 检索相关的想法节点           | `s_content`, `p_content`, `o_content`                                                                       | `ret`（集合，包含相关的想法节点）     |
| `retrieve_relevant_events`     | 检索相关的事件节点           | `s_content`, `p_content`, `o_content`                                                                       | `ret`（集合，包含相关的事件节点）     |
| `get_last_chat`                | 获取与特定对象的最后一次聊天 | `target_persona_name`                                                                                       | `chat`（最近的聊天节点或 False）      |

### 3.2. scratch

> `Scratch` 类定义了生成性代理人的短期记忆模块。它包含了代理人的当前状态、每日计划、当前动作、交谈信息等多个方面的信息，并提供了一系列方法来管理和操作这些信息。这些方法包括保存和加载代理人的状态、获取和设置每日计划的索引和内容、添加新动作、检查当前动作是否完成等。通过这些方法，`Scratch` 类实现了对代理人行为和状态的细致控制和跟踪。

**Scratch**

| 函数名称                                    | 函数作用                                        | 输入参数                                                                                                                                                                                                                                                      | 输出                                           |
| ------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `__init__`                                  | 初始化 Scratch 对象并加载已保存的状态。         | `f_saved`: 保存状态的文件路径                                                                                                                                                                                                                                 | 无                                             |
| `save`                                      | 保存当前代理人的 Scratch 状态。                 | `out_json`: 要保存状态的文件路径                                                                                                                                                                                                                              | 无                                             |
| `get_f_daily_schedule_index`                | 获取 `f_daily_schedule` 的当前索引。            | `advance=0`: 以分钟为单位向未来查看的整数值                                                                                                                                                                                                                   | 整数: `f_daily_schedule` 的当前索引            |
| `get_f_daily_schedule_hourly_org_index`     | 获取 `f_daily_schedule_hourly_org` 的当前索引。 | `advance=0`: 以分钟为单位向未来查看的整数值                                                                                                                                                                                                                   | 整数: `f_daily_schedule_hourly_org` 的当前索引 |
| `get_str_iss`                               | 返回代理人的身份稳定集摘要字符串。              | 无                                                                                                                                                                                                                                                            | 字符串: 身份稳定集摘要                         |
| `get_str_name`                              | 返回代理人的姓名。                              | 无                                                                                                                                                                                                                                                            | 字符串: 代理人的姓名                           |
| `get_str_firstname`                         | 返回代理人的名字。                              | 无                                                                                                                                                                                                                                                            | 字符串: 代理人的名字                           |
| `get_str_lastname`                          | 返回代理人的姓氏。                              | 无                                                                                                                                                                                                                                                            | 字符串: 代理人的姓氏                           |
| `get_str_age`                               | 返回代理人的年龄。                              | 无                                                                                                                                                                                                                                                            | 字符串: 代理人的年龄                           |
| `get_str_innate`                            | 返回代理人的先天特质。                          | 无                                                                                                                                                                                                                                                            | 字符串: 先天特质                               |
| `get_str_learned`                           | 返回代理人的后天特质。                          | 无                                                                                                                                                                                                                                                            | 字符串: 后天特质                               |
| `get_str_currently`                         | 返回代理人的当前状态。                          | 无                                                                                                                                                                                                                                                            | 字符串: 当前状态                               |
| `get_str_lifestyle`                         | 返回代理人的生活方式。                          | 无                                                                                                                                                                                                                                                            | 字符串: 生活方式                               |
| `get_str_daily_plan_req`                    | 返回代理人的每日计划要求。                      | 无                                                                                                                                                                                                                                                            | 字符串: 每日计划要求                           |
| `get_str_curr_date_str`                     | 返回当前日期字符串。                            | 无                                                                                                                                                                                                                                                            | 字符串: 当前日期                               |
| `get_curr_event`                            | 返回代理人当前从事的事件。                      | 无                                                                                                                                                                                                                                                            | 元组: 当前事件                                 |
| `get_curr_event_and_desc`                   | 返回当前事件及其描述。                          | 无                                                                                                                                                                                                                                                            | 元组: 当前事件和描述                           |
| `get_curr_obj_event_and_desc`               | 返回当前对象事件及其描述。                      | 无                                                                                                                                                                                                                                                            | 元组: 当前对象事件和描述                       |
| `add_new_action`                            | 向代理人的日程中添加新动作。                    | `action_address`, `action_duration`, `action_description`, `action_pronunciatio`, `action_event`, `chatting_with`, `chat`, `chatting_with_buffer`, `chatting_end_time`, `act_obj_description`, `act_obj_pronunciatio`, `act_obj_event`, `act_start_time=None` | 无                                             |
| `act_time_str`                              | 返回当前时间的字符串。                          | 无                                                                                                                                                                                                                                                            | 字符串: 当前时间                               |
| `act_check_finished`                        | 检查当前动作是否完成。                          | 无                                                                                                                                                                                                                                                            | 布尔值: 动作完成返回 True, 否则返回 False      |
| `act_summarize`                             | 将当前动作总结为字典。                          | 无                                                                                                                                                                                                                                                            | 字典: 动作的摘要                               |
| `act_summary_str`                           | 返回当前动作的字符串摘要。                      | 无                                                                                                                                                                                                                                                            | 字符串: 动作的摘要                             |
| `get_str_daily_schedule_summary`            | 返回每日计划摘要的字符串。                      | 无                                                                                                                                                                                                                                                            | 字符串: 每日计划摘要                           |
| `get_str_daily_schedule_hourly_org_summary` | 返回原始每日计划按小时划分的摘要字符串。        | 无                                                                                                                                                                                                                                                            | 字符串: 原始每日计划按小时划分的摘要           |

`Scratch` 类通过这些方法管理生成性代理人的短期记忆和当前状态，实现对代理人行为和状态的细致控制和跟踪。

### 3.3. spatial_memory

> `MemoryTree` 类定义了一个用于代理人的空间记忆的类，它帮助代理人在游戏世界中进行行为定位。该类通过树形结构存储空间信息，并提供一系列方法来操作和获取这些信息，包括获取可访问的部门、区域以及游戏对象等。`MemoryTree` 类确保代理人在执行任务时能够准确地找到和利用环境中的资源。

**MemoryTree**

| 函数名称                                | 函数作用                                               | 输入参数                               | 输出                             |
| --------------------------------------- | ------------------------------------------------------ | -------------------------------------- | -------------------------------- |
| `__init__`                              | 初始化 `MemoryTree` 对象并加载已保存的树结构。         | `f_saved`: 保存树结构的文件路径        | 无                               |
| `print_tree`                            | 打印当前的树结构。                                     | 无                                     | 无                               |
| `save`                                  | 保存当前的树结构到指定文件。                           | `out_json`: 要保存树结构的文件路径     | 无                               |
| `get_str_accessible_sectors`            | 返回代理人当前世界中所有可访问的部门的摘要字符串。     | `curr_world`: 代理人当前所在的世界名称 | 字符串: 所有可访问部门的摘要     |
| `get_str_accessible_sector_arenas`      | 返回代理人当前部门中所有可访问的区域的摘要字符串。     | `sector`: 代理人当前所在的部门名称     | 字符串: 所有可访问区域的摘要     |
| `get_str_accessible_arena_game_objects` | 返回代理人当前区域中所有可访问的游戏对象的摘要字符串。 | `arena`: 代理人当前所在的区域名称      | 字符串: 所有可访问游戏对象的摘要 |

`MemoryTree` 类通过这些方法管理生成性代理人的空间记忆，实现对代理人在游戏世界中的行为定位和资源利用。

