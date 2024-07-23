# 短时记忆模块（Scratch Memory Module）

该脚本定义了一个用于生成型代理（generative agents）的短时记忆模块 `Scratch`。这个模块管理代理的即时状态、计划和行动。

## 1. 核心类和方法

### 1.1 Scratch 类

`Scratch` 类管理代理的短期记忆和当前状态，包括视觉范围、注意力带宽、记忆保持时间、当前时间和位置、日常计划等信息。

#### 1.1.1 初始化方法 `__init__`
- **输入参数**：
  - `f_saved`：存储文件路径，用于加载代理的状态。
- **主要属性**：
  - `vision_r`：视觉范围，表示代理可以看到周围的格子数量。
  - `att_bandwidth`：注意力带宽。
  - `retention`：记忆保持时间。
  - `curr_time`：当前时间。
  - `curr_tile`：当前的 x, y 坐标。
  - `daily_plan_req`：每日计划需求。
  - 代理的核心身份信息，包括名字、年龄、特质等。
  - 反思变量，用于管理代理的反思过程。
  - 每日计划和日程安排。
  - 当前行动的详细信息。

#### 1.1.2 保存方法 `save`

```python
def save(self, out_json):
    """
    保存代理的当前状态。

    输入：
      out_json：保存状态的文件路径。
    输出：
      None
    """
```
- 将当前状态保存到指定文件路径 `out_json`。

#### 1.1.3 获取日程索引方法 `get_f_daily_schedule_index` 和 `get_f_daily_schedule_hourly_org_index`
- `get_f_daily_schedule_index(advance=0)`：获取当前 `f_daily_schedule` 的索引，可以根据 `advance` 参数提前查看未来的时间点。
- `get_f_daily_schedule_hourly_org_index(advance=0)`：与 `get_f_daily_schedule_index` 类似，但针对 `f_daily_schedule_hourly_org`。

#### 1.1.4 获取身份稳定集字符串 `get_str_iss`

```python
def get_str_iss(self):
    """
    返回代理的身份稳定集字符串。

    输入：
      None
    输出：
      身份稳定集的字符串表示。
    """
```
- 返回代理的身份稳定集（ISS），描述代理的基本信息和日常计划。

#### 1.1.5 获取代理基本信息字符串
- `get_str_name()`：返回代理的名字。
- `get_str_firstname()`：返回代理的名字。
- `get_str_lastname()`：返回代理的姓氏。
- `get_str_age()`：返回代理的年龄。
- `get_str_innate()`：返回代理的先天特质。
- `get_str_learned()`：返回代理的习得特质。
- `get_str_currently()`：返回代理当前的状态。
- `get_str_lifestyle()`：返回代理的生活方式。
- `get_str_daily_plan_req()`：返回代理的日常计划需求。
- `get_str_curr_date_str()`：返回当前日期的字符串。

#### 1.1.6 获取当前事件和描述
- `get_curr_event()`：返回当前事件的三元组 (SPO)。
- `get_curr_event_and_desc()`：返回当前事件的三元组和描述。
- `get_curr_obj_event_and_desc()`：返回当前对象事件的三元组和描述。

#### 1.1.7 添加新行动 `add_new_action`

```python
def add_new_action(self, action_address, action_duration, action_description, action_pronunciatio, action_event, chatting_with, chat, chatting_with_buffer, chatting_end_time, act_obj_description, act_obj_pronunciatio, act_obj_event, act_start_time=None):
    """
    添加一个新的行动。

    输入参数包括行动的详细信息、聊天对象、聊天内容等。
    """
```
- 更新当前行动的相关属性。

#### 1.1.8 获取当前时间字符串 `act_time_str`

```python
def act_time_str(self):
    """
    返回当前时间的字符串表示。

    输入：
      None
    输出：
      当前时间的字符串表示。
    """
```

#### 1.1.9 检查行动是否完成 `act_check_finished`

```python
def act_check_finished(self):
    """
    检查当前行动是否完成。

    输入：
      None
    输出：
      布尔值 [True]：行动已完成。
      布尔值 [False]：行动未完成，仍在进行中。
    """
```

#### 1.1.10 总结当前行动 `act_summarize`

```python
def act_summarize(self):
    """
    总结当前行动为字典。

    输入：
      None
    输出：
      当前行动的可读摘要。
    """
```

#### 1.1.11 获取当前行动字符串摘要 `act_summary_str`

```python
def act_summary_str(self):
    """
    返回当前行动的字符串摘要。旨在可读性。

    输入：
      None
    输出：
      当前行动的可读摘要字符串。
    """
```

#### 1.1.12 获取每日计划摘要字符串
- `get_str_daily_schedule_summary()`：返回 `f_daily_schedule` 的字符串摘要。
- `get_str_daily_schedule_hourly_org_summary()`：返回 `f_daily_schedule_hourly_org` 的字符串摘要。

## 2. 总结

`Scratch` 类是生成型代理的短时记忆模块，管理代理的当前状态、日常计划和行动。它提供了丰富的方法来添加和更新代理的行动，获取代理的基本信息和当前状态，以及保存和加载代理的状态。这个模块在生成型代理的即时决策和行为管理中起着关键作用。
