# 脚本功能概述

该脚本定义了生成型代理（generative agents）的 "Retrieve" 模块，用于从代理的记忆中检索与当前感知到的事件相关的记忆和思考。通过计算事件和思考的相似性和重要性，帮助代理在规划时考虑相关的上下文信息。

## 1. 核心类和方法

### 1.1 全局方法

#### 1.1.1 检索方法 `retrieve`

```python
def retrieve(persona, perceived):
    """
    根据代理感知到的事件，返回代理需要在规划时考虑的相关事件和思考。

    输入：
      persona: 当前代理的实例。
      perceived: 一个包含感知到的事件 <ConceptNode> 的列表。

    输出：
      retrieved: 一个字典，包含与感知到的事件相关的当前事件、相关事件和相关思考。
    """
```
- **功能**：根据代理感知到的事件，检索相关的事件和思考，返回包含这些信息的字典。
- **输入参数**：
  - `persona`：当前代理实例。
  - `perceived`：感知到的事件列表。
- **输出**：返回包含相关事件和思考的字典。

#### 1.1.2 余弦相似度计算方法 `cos_sim`

```python
def cos_sim(a, b):
    """
    计算两个向量 a 和 b 之间的余弦相似度。

    输入：
      a: 1-D 数组
      b: 1-D 数组

    输出：
      表示输入向量之间余弦相似度的标量值。
    """
```
- **功能**：计算两个向量之间的余弦相似度，用于衡量它们的相似性。
- **输入参数**：
  - `a`：1-D 数组。
  - `b`：1-D 数组。
- **输出**：返回余弦相似度的标量值。

#### 1.1.3 字典值归一化方法 `normalize_dict_floats`

```python
def normalize_dict_floats(d, target_min, target_max):
    """
    将字典 d 的浮点值归一化到目标最小值和最大值之间。

    输入：
      d: 字典，包含需要归一化的浮点值。
      target_min: 目标最小值。
      target_max: 目标最大值。

    输出：
      归一化后的新字典。
    """
```
- **功能**：将字典中的浮点值归一化到指定的范围。
- **输入参数**：
  - `d`：字典。
  - `target_min`：目标最小值。
  - `target_max`：目标最大值。
- **输出**：返回归一化后的字典。

#### 1.1.4 提取最高值方法 `top_highest_x_values`

```python
def top_highest_x_values(d, x):
    """
    提取字典 d 中值最高的前 x 个键值对。

    输入：
      d: 字典。
      x: 要提取的键值对数量。

    输出：
      包含值最高的前 x 个键值对的新字典。
    """
```
- **功能**：提取字典中值最高的前 x 个键值对。
- **输入参数**：
  - `d`：字典。
  - `x`：要提取的键值对数量。
- **输出**：返回包含值最高的前 x 个键值对的字典。

#### 1.1.5 提取最近性分数方法 `extract_recency`

```python
def extract_recency(persona, nodes):
    """
    计算节点列表的最近性分数。

    输入：
      persona: 当前代理。
      nodes: 按时间顺序排列的节点列表。

    输出：
      包含节点最近性分数的字典。
    """
```
- **功能**：计算节点的最近性分数，用于衡量节点的时间相关性。
- **输入参数**：
  - `persona`：当前代理实例。
  - `nodes`：按时间顺序排列的节点列表。
- **输出**：返回包含节点最近性分数的字典。

#### 1.1.6 提取重要性分数方法 `extract_importance`

```python
def extract_importance(persona, nodes):
    """
    计算节点列表的重要性分数。

    输入：
      persona: 当前代理。
      nodes: 按时间顺序排列的节点列表。

    输出：
      包含节点重要性分数的字典。
    """
```
- **功能**：计算节点的重要性分数，用于衡量节点的重要性。
- **输入参数**：
  - `persona`：当前代理实例。
  - `nodes`：按时间顺序排列的节点列表。
- **输出**：返回包含节点重要性分数的字典。

#### 1.1.7 提取相关性分数方法 `extract_relevance`

```python
def extract_relevance(persona, nodes, focal_pt):
    """
    计算节点列表的相关性分数。

    输入：
      persona: 当前代理。
      nodes: 按时间顺序排列的节点列表。
      focal_pt: 当前焦点的描述。

    输出：
      包含节点相关性分数的字典。
    """
```
- **功能**：计算节点的相关性分数，用于衡量节点与当前焦点的相关性。
- **输入参数**：
  - `persona`：当前代理实例。
  - `nodes`：按时间顺序排列的节点列表。
  - `focal_pt`：当前焦点的描述。
- **输出**：返回包含节点相关性分数的字典。

#### 1.1.8 新检索方法 `new_retrieve`

```python
def new_retrieve(persona, focal_points, n_count=30):
    """
    根据代理和焦点检索相关节点。

    输入：
      persona: 当前代理实例。
      focal_points: 焦点列表。
      n_count: 检索节点的数量。

    输出：
      包含焦点和相关节点的字典。
    """
```
- **功能**：根据代理的记忆和当前焦点，检索相关的节点，并返回包含这些信息的字典。
- **输入参数**：
  - `persona`：当前代理实例。
  - `focal_points`：焦点列表。
  - `n_count`：检索的节点数量。
- **输出**：返回包含焦点和相关节点的字典。

## 2. 示例代码

```python
if __name__ == "__main__":
    from persona import Persona

    persona = Persona("example_persona")
    perceived = [event1, event2, event3]  # 示例事件列表

    retrieved_events = retrieve(persona, perceived)
    print(retrieved_events)

    focal_points = ["How are you?", "Jane is swimming in the pond"]
    retrieved_nodes = new_retrieve(persona, focal_points)
    print(retrieved_nodes)
```

## 3. 总结

`retrieve.py` 脚本定义了生成型代理的检索模块，通过感知代理周围的事件，检索与这些事件相关的记忆和思考。它包括计算事件和思考的相似性、重要性和相关性的方法，帮助代理在规划时考虑相关的上下文信息。这种检索能力使得代理能够在虚拟世界中更加智能地做出决策和行动。
