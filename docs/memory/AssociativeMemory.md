# Associative Memory / 长时记忆模块

该脚本通过定义 `ConceptNode` 和 `AssociativeMemory` 类，实现了一个长时记忆模块，用于生成型代理（generative agents）。记忆节点分为三种类型：事件（Event）、对话（Chat）和反思（Thought）。以下是详细的功能说明。

## 1. 核心类和方法

### 1.1 ConceptNode 类

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

### 1.2. AssociativeMemory 类

`AssociativeMemory` 类管理多个 `ConceptNode` 节点，并提供以下功能：

#### 1.2.1 初始化方法

```python
__init__(self, f_saved)
```
- 从文件 `f_saved` 加载嵌入、节点和关键词强度信息，构建内存中的节点和相关字典映射。

#### 1.2.2 保存方法

```python
save(self, out_json)
```
- 将当前节点和关键词强度信息保存到指定路径 `out_json`。

#### 1.2.3 添加节点方法

- `add_event(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`:
    添加一个新的事件节点，并更新相关字典和序列。
- `add_chat(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`:
    添加一个新的对话节点，并更新相关字典和序列。
- `add_thought(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`:
    添加一个新的反思节点，并更新相关字典和序列。

#### 1.2.4 信息检索方法

- `retrieve_relevant_thoughts(self, s_content, p_content, o_content)`:
    根据`关键词检索`相关的思考节点。
- `retrieve_relevant_events(self, s_content, p_content, o_content)`:
    根据`关键词检索`相关的事件节点。
- `get_last_chat(self, target_persona_name)`:
    获取与指定人物的最后一次聊天记录。

#### 1.2.5 获取字符串序列方法

- `get_str_seq_events(self)`:
    获取事件的字符串序列表示。
- `get_str_seq_thoughts(self)`:
    获取反思的字符串序列表示。
- `get_str_seq_chats(self)`:
    获取对话的字符串序列表示。

#### 1.2.6 获取最新事件摘要方法

- `get_summarized_latest_events(self, retention)`: 获取最近一段时间的事件摘要。

## 2.  三种类型的记忆节点

### 2.1. 事件（Event）

**存储方式**：
- 事件被添加到 `seq_event` 序列中，按时间顺序存储。
- 每个事件节点包含创建时间、过期时间、三元组 (SPO)、描述、关键词等信息。
- 事件节点也会更新关键词到事件的映射字典 `kw_to_event`，便于后续检索。

**方法**：
- `add_event(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`

### 2.2. 对话（Chat）

**存储方式**：
- 对话被添加到 `seq_chat` 序列中，按时间顺序存储。
- 每个对话节点包含创建时间、过期时间、三元组 (SPO)、描述、关键词以及填充对话的内容。
- 对话节点也会更新关键词到对话的映射字典 `kw_to_chat`，便于后续检索。

**方法**：
- `add_chat(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`

### 2.3. 反思（Thought）

**存储方式**：
- 反思被添加到 `seq_thought` 序列中，按时间顺序存储。
- 每个反思节点包含创建时间、过期时间、三元组 (SPO)、描述、关键词等信息。
- 反思节点也会更新关键词到反思的映射字典 `kw_to_thought`，便于后续检索。

**方法**：
- `add_thought(self, created, expiration, s, p, o, description, keywords, poignancy, embedding_pair, filling)`

## 3. 总结

该脚本通过 `ConceptNode` 和 `AssociativeMemory` 类，定义并管理三种类型的记忆节点：事件（Event）、对话（Chat）和反思（Thought）。这些节点的添加、存储和检索方式使得生成型代理能够有效地管理和利用其长时记忆。
