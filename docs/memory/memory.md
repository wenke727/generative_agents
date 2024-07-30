# Memory

### ConceptNode 类

`ConceptNode` 类表示一个记忆节点，节点可以是事件、思考或聊天。每个节点包含：

- **node_id**：节点唯一标识符
- **node_count**：节点总数
- **type_count**：节点类型计数
- **type**：节点类型（thought/event/chat）
- **depth**：节点深度
- **created**：节点创建时间
- **expiration**：节点过期时间
- **last_accessed**：最后访问时间
- **subject**、**predicate**、**object**：三元组 (SPO)
- **description**：节点描述
- **embedding_key**：嵌入键
- **poignancy**：节点的重要性
- **keywords**：关键词集合
- **filling**：填充信息

#### 1.1.1 方法

- `spo_summary()`: 返回节点的三元组 (SPO) 摘要。

## Scratch Memory Module

| Name                   | Desc                            | 调用                            |
| ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| get_f_daily_schedule_index        | 获取当前  `f_daily_schedule` 的索引             | plan._determine_action                   |
| get_f_daily_schedule_hourly_org_index  | 与  `get_f_daily_schedule_index` 类似，但针对 `f_daily_schedule_hourly_org` | plan._create_react                     |
| get_str_iss               | 身份稳定集字符串                      | plan._revise_identity<br />run_gpt_prompt_wake_up_hour<br />run_gpt_prompt_daily_plan<br />run_gpt_prompt_generate_hourly_schedule<br />run_gpt_prompt_task_decomp<br />run_gpt_prompt_event_poignancy<br />run_gpt_prompt_thought_poignancy<br />run_gpt_prompt_chat_poignancy<br />run_gpt_prompt_create_conversation<br />run_gpt_prompt_generate_next_convo_line<br />run_gpt_generate_iterative_chat_utt |
|                     |                               |                               |
| get_curr_event              | 返回当前事件的三元组 (SPO)                 | --                             |
| get_curr_event_and_desc         | 返回当前事件的三元组和描述                 | 和 maze 交互                        |
| get_curr_obj_event_and_desc       | 返回当前对象事件的三元组和描述               | reverie.ReverieServer.start_server             |
|                     |                               |                               |
| add_new_action              | 添加新行动                         | plan._determine_action<br />plan._create_react       |
| act_time_str               | 获取当前时间字符串                     | --                             |
| act_check_finished            | 检查行动是否完成                      | plan.plan                          |
| act_summarize              | 总结当前行动                        | --                             |
| act_summary_str             | 获取当前行动字符串摘要                   | --                             |
| get_str_daily_schedule_summary      | 返回  `f_daily_schedule` 的字符串摘要            | reverie.ReverieServer.open_server              |
| get_str_daily_schedule_hourly_org_summary | 返回  `f_daily_schedule_hourly_org` 的字符串摘要       | reverie.ReverieServer.open_server              |

## Spatial Memory


| Name         | Desc            | 调用              |
| ------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| get_str_accessible_sectors   | 返回代理在当前世界中可访问的所有区域的摘要字符串 | run_gpt_prompt_action_sector -> plan._determine_action  |
| get_str_accessible_sector_arenas  | 返回代理在当前区域中可访问的所有子区域的摘要字符串 | run_gpt_prompt_action_sector<br />run_gpt_prompt_action_arena -> plan._determine_action |
| get_str_accessible_arena_game_objects | 获取在指定竞技场中可访问的所有游戏对象的字符串列表 | plan._generate_action_game_object<br />run_gpt_prompt_action_game_object |

## Associative Memory

| Name      | Desc       | 调用              |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------ |
| add_event     | 添加一个新的**事件**节点  | perceive.perceive           |
| add_chat     | 添加一个新的**对话**节点  | perceive.perceive           |
| add_thought     | 添加一个新的**反思**节点  | converse.load_history_via_whisper<br />converse.open_convo_session<br />plan._long_term_planning<br />reflect.run_reflect<br />reflect.reflect |
| get_summarized_latest_events | 获取最近一段时间的事件摘要  | perceive.perceive           |
| retrieve_relevant_events | 根据关键词检索相关的事件节点 | retrieve.retrieve           |
| retrieve_relevant_thoughts | 根据关键词检索相关的思考节点 | retrieve.retrieve<br />run_gpt_prompt_create_conversation |
| get_last_chat    | 获取与指定人物的最后一次聊天记录 | reflect.reflect<br />run_gpt_prompt_decide_to_talk   |