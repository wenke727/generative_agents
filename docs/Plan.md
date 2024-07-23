# Plan 模块

## 脚本功能概述

`plan.py` 脚本定义了生成型代理（generative agents）的 "Plan" 模块。该模块负责生成代理的日常计划，包括长短期计划，反应计划，以及与其他代理的互动计划。通过与 GPT-3 模型交互生成代理的每日活动计划，并基于代理的感知和检索到的信息进行相应的反应。

## 1. 核心类和方法

### 1.1 生成相关的方法

#### 1.1.1 生成起床时间 `generate_wake_up_hour`

```python
def generate_wake_up_hour(persona):
    """
    生成代理的起床时间。

    输入：
      persona: 代理实例。

    输出：
      起床时间（小时）。
    """
```

- **功能**：生成代理的起床时间。
- **输入参数**：`persona` 当前代理实例。
- **输出**：返回代理的起床时间（小时）。

#### 1.1.2 生成每日计划 `generate_first_daily_plan`

```python
def generate_first_daily_plan(persona, wake_up_hour):
    """
    生成代理的每日计划。

    输入：
      persona: 代理实例。
      wake_up_hour: 起床时间。

    输出：
      每日计划列表。
    """
```

- **功能**：生成代理的每日计划。
- **输入参数**：
  - `persona`：当前代理实例。
  - `wake_up_hour`：起床时间。
- **输出**：返回每日计划列表。

#### 1.1.3 生成每小时计划 `generate_hourly_schedule`

```python
def generate_hourly_schedule(persona, wake_up_hour):
    """
    基于每日计划生成每小时的活动计划。

    输入：
      persona: 代理实例。
      wake_up_hour: 起床时间。

    输出：
      每小时计划列表。
    """
```

- **功能**：生成代理的每小时计划。
- **输入参数**：
  - `persona`：当前代理实例。
  - `wake_up_hour`：起床时间。
- **输出**：返回每小时计划列表。

#### 1.1.4 生成任务分解 `generate_task_decomp`

```python
def generate_task_decomp(persona, task, duration):
    """
    将任务分解为更小的子任务。

    输入：
      persona: 代理实例。
      task: 任务描述。
      duration: 任务持续时间。

    输出：
      子任务列表。
    """
```

- **功能**：将任务分解为更小的子任务。
- **输入参数**：
  - `persona`：当前代理实例。
  - `task`：任务描述。
  - `duration`：任务持续时间。
- **输出**：返回子任务列表。

#### 1.1.5 生成行动部门 `generate_action_sector`

```python
def generate_action_sector(act_desp, persona, maze):
    """
    根据任务描述生成行动部门。

    输入：
      act_desp: 任务描述。
      persona: 代理实例。
      maze: 当前迷宫实例。

    输出：
      行动部门。
    """
```

- **功能**：根据任务描述生成行动部门。
- **输入参数**：
  - `act_desp`：任务描述。
  - `persona`：当前代理实例。
  - `maze`：当前迷宫实例。
- **输出**：返回行动部门。

#### 1.1.6 生成行动场景 `generate_action_arena`

```python
def generate_action_arena(act_desp, persona, maze, act_world, act_sector):
    """
    根据任务描述生成行动场景。

    输入：
      act_desp: 任务描述。
      persona: 代理实例。
      maze: 当前迷宫实例。
      act_world: 行动世界。
      act_sector: 行动部门。

    输出：
      行动场景。
    """
```

- **功能**：根据任务描述生成行动场景。
- **输入参数**：
  - `act_desp`：任务描述。
  - `persona`：当前代理实例。
  - `maze`：当前迷宫实例。
  - `act_world`：行动世界。
  - `act_sector`：行动部门。
- **输出**：返回行动场景。

#### 1.1.7 生成行动对象 `generate_action_game_object`

```python
def generate_action_game_object(act_desp, act_address, persona, maze):
    """
    根据任务描述生成行动对象。

    输入：
      act_desp: 任务描述。
      act_address: 行动地址。
      persona: 代理实例。
      maze: 当前迷宫实例。

    输出：
      行动对象。
    """
```

- **功能**：根据任务描述生成行动对象。
- **输入参数**：
  - `act_desp`：任务描述。
  - `act_address`：行动地址。
  - `persona`：当前代理实例。
  - `maze`：当前迷宫实例。
- **输出**：返回行动对象。

#### 1.1.8 生成行动描述 `generate_act_obj_desc`

```python
def generate_act_obj_desc(act_game_object, act_desp, persona):
    """
    生成行动对象描述。

    输入：
      act_game_object: 行动对象。
      act_desp: 任务描述。
      persona: 代理实例。

    输出：
      行动对象描述。
    """
```

- **功能**：生成行动对象描述。
- **输入参数**：
  - `act_game_object`：行动对象。
  - `act_desp`：任务描述。
  - `persona`：当前代理实例。
- **输出**：返回行动对象描述。

### 1.2 计划模块方法

#### 1.2.1 计划主方法 `plan`

```python
def plan(persona, maze, personas, new_day, retrieved):
    """
    主计划方法，根据检索到的信息生成代理的短期和长期计划。

    输入：
      persona: 当前代理实例。
      maze: 当前迷宫实例。
      personas: 代理字典。
      new_day: 新的一天。
      retrieved: 检索到的记忆和感知信息。

    输出：
      目标行动地址。
    """
```

- **功能**：生成代理的短期和长期计划。
- **输入参数**：
  - `persona`：当前代理实例。
  - `maze`：当前迷宫实例。
  - `personas`：代理字典。
  - `new_day`：新的一天。
  - `retrieved`：检索到的记忆和感知信息。
- **输出**：返回目标行动地址。

#### 1.2.2 长期计划方法 `_long_term_planning`

```python
def _long_term_planning(persona, new_day):
    """
    为代理生成长期计划。

    输入：
      persona: 当前代理实例。
      new_day: 新的一天。

    输出：
      None
    """
```

- **功能**：为代理生成长期计划。
- **输入参数**：
  - `persona`：当前代理实例。
  - `new_day`：新的一天。

#### 1.2.3 短期计划方法 `_determine_action`

```python
def _determine_action(persona, maze):
    """
    生成代理的下一步行动计划。

    输入：
      persona: 当前代理实例。
      maze: 当前迷宫实例。

    输出：
      None
    """
```

- **功能**：生成代理的下一步行动计划。
- **输入参数**：
  - `persona`：当前代理实例。
  - `maze`：当前迷宫实例。

## 2. 示例代码

```python
if __name__ == "__main__":
    from persona import Persona
    from maze import Maze

    persona = Persona("example_persona")
    maze = Maze()
    personas = {"example_persona": persona}

    new_day = "First day"
    retrieved = {}  # 示例的检索数据

    plan(persona, maze, personas, new_day, retrieved)
```

## 3. 总结

`plan.py` 脚本定义了生成型代理的计划模块，通过生成每日活动计划和反应计划，使代理能够在虚拟世界中智能地进行长短期决策和行动。该模块与 GPT-3 模型交互生成计划，并根据代理的感知和检索信息调整计划，从而提升代理的智能性和适应性。
