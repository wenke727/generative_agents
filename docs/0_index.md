# Index



## Persona

> `Persona` 类定义了在 Reverie 中为代理人提供动力的基本行为和认知功能。这个类主要包括处理代理人记忆、感知、计划、执行和反思的功能模块。通过与各种记忆结构和认知模块的交互，`Persona` 类能够模拟一个代理人的日常行为和决策过程。

| 函数名称             | 作用                                           | 输入参数                                                     | 输出参数                                                     |
| -------------------- | ---------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `__init__`           | 初始化代理人的基本状态和记忆结构               | `name`: 代理人的名字<br>`folder_mem_saved`: 存储记忆的文件夹路径 | 无                                                           |
| `save`               | 保存代理人的当前状态（记忆）                   | `save_folder`: 保存代理人状态的文件夹路径                    | 无                                                           |
| `perceive`           | 感知当前迷宫中的事件，返回代理人周围发生的事件 | `maze`: 当前世界的迷宫实例                                   | 一个包含新感知到的 <ConceptNode> 列表                        |
| `retrieve`           | 从记忆中检索与感知事件相关的事件和想法         | `perceived`: 一个包含新感知到的 <ConceptNode> 列表           | 一个字典，包含相关的事件和想法                               |
| `plan`               | 进行代理人的长期和短期计划                     | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`new_day`: 这可以取三个值之一<br>&nbsp;&nbsp;&nbsp;&nbsp;1) <Boolean> False - 不是“新的一天”周期<br>&nbsp;&nbsp;&nbsp;&nbsp;2) <String> "First day" - 实际上是模拟的开始，所以不仅是新的一天，也是第一天<br>&nbsp;&nbsp;&nbsp;&nbsp;3) <String> "New day" - 是新的一天。<br>`retrieved`: 包含相关事件和想法的字典 | 代理人的目标动作地址（`persona.scratch.act_address`）        |
| `reflect`            | 回顾代理人的记忆，并基于记忆创建新的想法       | 无                                                           | 无                                                           |
| `execute`            | 执行当前计划，输出具体的执行步骤               | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`plan`: 代理人的目标动作地（`persona.scratch.act_address`） | 一个三元组，包含以下组件：<br>`next_tile`: x,y 坐标<br>`pronunciatio`: 表情符号<br>`description`: 动作描述 |
| `move`               | 代理人的主要认知函数，调用主要的认知序列;      | `maze`: 当前世界的迷宫实例<br>`personas`: 包含所有代理人的字典<br>`curr_tile`: 当前的x,y坐标<br>`curr_time`: 当前时间实例 | 一个三元组，包含以下组件：<br>`next_tile`: x,y 坐标<br>`pronunciatio`: 表情符号<br>`description`: 动作描述 |
| `open_convo_session` | 打开对话会话                                   | `convo_mode`: 对话模式                                       | 无                                                           |

<img src="https://img.huxiucdn.com/article/content/202308/10/132522252516.png?imageView2/2/w/1000/format/png/interlace/1/q/85" style="zoom:67%;" />

## Ability

- [ ] [感知](./Perceive.md)
- [x] [检索](./Retrieve.md)
- [ ] [计划](./Plan.md)
- [ ] [反思](./Reflect.md)
- [ ] [执行](./Execute.md)
- [ ] [对话](./Converse.md)

## [Memory](./memory/memory.md)

- [x] [长期记忆模块](./memory/AssociativeMemory.md)
- [x] [短期记忆模块](./memory/ScratchMemoryModule.md)
- [x] [空间记忆模块](./memory/SpaceMemory.md)

##
