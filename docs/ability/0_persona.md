# Persona

## 基础框架

> `Persona` 类定义了在 Reverie 中为代理人提供动力的基本行为和认知功能。
>
> 这个类主要包括处理代理人记忆、感知、计划、执行和反思的功能模块。通过与各种记忆结构和认知模块的交互，`Persona` 类能够模拟一个代理人的日常行为和决策过程。

## 主函数

主循环会调用每个 Persona 类的 move 方法

<img src="https://developer.qcloudimg.com/http-save/yehe-admin/b259fddbd3a6adcead2162843bb8d9a0.png" style="zoom:50%;" />

<img src="https://developer.qcloudimg.com/http-save/yehe-admin/9c69b2f5000be2c221fcaffcae768ac2.png" alt="img" style="zoom:50%;" />

可以看到 move 方法通过当前的地图状态、agent 列表、以及当前的时间和位置 -> 决定Agent 行为

该方法的流程具体可分为：

1. 根据时间判断当前是否为新的一天(或更特别的，为第一天)，当为新的一天时需要进行长期/当日计划，这一点与人类的习惯相符
2. 调用`perceive`方法（感知），此方法用于感知Agent当前周围正在发生的事情，并根据发生的范围对其进行排序，返回一个 ConceptNode 列表
3. 调用`retrieve`方法，根据perceive方法得到用户感知到的想法，即 ConceptNode 列表作为输入，输出一组经过排序的相关的`事件`和`想法`
4. 调用`plan`方法（计划），此方法即模仿人类的思考过程，以 retrieve 方法的输出作为输入。整体上分为几个阶段：
   - 如果是新的一天，进行长期规划
   - 如果当前动作停止，决定下一个进行的动作
   - 根据目前感知到的事件，决定当前专注于其中哪一件
   - 对于目前专注的事件，决定进行什么动作（有三种动作：与某人交谈、对事件进行反应、不对事件进行反应）
5. 调用`reflect`方法，这里翻译成中文应该叫“反思”，同样参考[这篇文章](https://cloud.tencent.com/developer/tools/blog-entry?target=https%3A%2F%2Fzhuanlan.zhihu.com%2Fp%2F649991229&source=article&objectId=2329791)对反思这个概念的解释; 通俗的来说，上面的思考流程都是浅层次的对事件的感知和反应，但人类有更高层次的总结、提炼、发掘潜在意图等思考方式，“反思”即模拟这种思考方式，对近段时间发生的事件进行更高层次的思考，并将思考结果作为记忆流的一部分存储起来
6. 调用execute方法，到这一步Agent已经决定了自己要做的事情，在execute方法中会根据目的地选择最优路径，或者是原地等待等

## 函数

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
