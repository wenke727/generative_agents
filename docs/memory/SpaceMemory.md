# 空间记忆模块（Spatial Memory Module）

该脚本定义了一个用于生成型代理（generative agents）的空间记忆模块 `MemoryTree`，帮助代理在游戏世界中定位和行为。

## 1. 核心类和方法

### 1.1 MemoryTree 类

`MemoryTree` 类管理代理的空间记忆，使用树形结构存储和检索位置和物体信息。

#### 1.1.1 初始化方法 `__init__`
- **输入参数**：
  - `f_saved`：存储文件路径，用于加载树形结构数据。
- **主要属性**：
  - `tree`：树形结构，表示空间记忆。
- **功能**：
  - 检查文件是否存在，如果存在则加载树形结构数据。

#### 1.1.2 打印树形结构方法 `print_tree`

```python
def print_tree(self):
    def _print_tree(tree, depth):
        dash = " >" * depth
        if type(tree) == type(list()):
            if tree:
                print(dash, tree)
            return

        for key, val in tree.items():
            if key:
                print(dash, key)
            _print_tree(val, depth + 1)

    _print_tree(self.tree, 0)
```
- 打印树形结构，展示空间记忆的层次关系。

#### 1.1.3 保存方法 `save`

```python
def save(self, out_json):
    with open(out_json, "w") as outfile:
        json.dump(self.tree, outfile)
```
- 将当前树形结构保存到指定文件路径 `out_json`。

#### 1.1.4 获取可访问区域字符串 `get_str_accessible_sectors`

```python
def get_str_accessible_sectors(self, curr_world):
    """
    返回代理在当前世界中可访问的所有区域的摘要字符串。

    输入：
      curr_world：当前世界名称。
    输出：
      代理可访问的所有区域的摘要字符串。
    示例输出：
      "bedroom, kitchen, dining room, office, bathroom"
    """
    x = ", ".join(list(self.tree[curr_world].keys()))
    return x
```
- 返回代理在当前世界中可访问的所有区域的摘要字符串。

#### 1.1.5 获取可访问区域的子区域字符串 `get_str_accessible_sector_arenas`

```python
def get_str_accessible_sector_arenas(self, sector):
    """
    返回代理在当前区域中可访问的所有子区域的摘要字符串。

    输入：
      sector：当前区域名称（格式为 "world:sector"）。
    输出：
      代理可访问的所有子区域的摘要字符串。
    示例输出：
      "bedroom, kitchen, dining room, office, bathroom"
    """
    curr_world, curr_sector = sector.split(":")
    if not curr_sector:
        return ""
    x = ", ".join(list(self.tree[curr_world][curr_sector].keys()))
    return x
```
- 返回代理在当前区域中可访问的所有子区域的摘要字符串。

#### 1.1.6 获取可访问游戏对象字符串 `get_str_accessible_arena_game_objects`

```python
def get_str_accessible_arena_game_objects(self, arena):
    """
    获取在指定竞技场中可访问的所有游戏对象的字符串列表。

    输入：
      arena：当前竞技场名称（格式为 "world:sector:arena"）。
    输出：
      可访问的所有游戏对象的字符串列表。
    示例输出：
      "phone, charger, bed, nightstand"
    """
    curr_world, curr_sector, curr_arena = arena.split(":")

    if not curr_arena:
        return ""

    try:
        x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena]))
    except:
        x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena.lower()]))
    return x
```
- 获取在指定竞技场中可访问的所有游戏对象的字符串列表。

### 1.2 主函数

```python
if __name__ == "__main__":
    fn = f"../../../../environment/frontend_server/storage/base_the_ville_n25/personas/Eddy Lin/bootstrap_memory/spatial_memory.json"
    x = MemoryTree(fn)
    x.print_tree()

    print(x.get_str_accessible_sector_arenas("dolores double studio:double studio"))
```
- 主函数用于加载树形结构数据并测试方法，打印树形结构和当前区域中可访问的所有子区域。

### 1.3 Data Demo

```python 
{
    "the Ville": {
        "Hobbs Cafe": {
            "cafe": [
                "refrigerator",
                "cafe customer seating",
                "cooking area",
                "kitchen sink",
                "behind the cafe counter",
                "piano"
            ]
        },
        "Isabella Rodriguez's apartment": {
            "main room": [
                "bed",
                "desk",
                "refrigerator",
                "closet",
                "shelf"
            ],
            "bathroom": [
                "shower",
                "bathroom sink",
                "toilet"
            ]
        },
        "The Rose and Crown Pub": {
            "pub": [
                "shelf",
                "refrigerator",
                "bar customer seating",
                "behind the bar counter",
                "kitchen sink",
                "cooking area",
                "microphone"
            ]
        },
        "Harvey Oak Supply Store": {
            "supply store": [
                "supply store product shelf",
                "behind the supply store counter",
                "supply store counter"
            ]
        },
        "The Willows Market and Pharmacy": {
            "store": [
                "behind the pharmacy counter",
                "pharmacy store shelf",
                "pharmacy store counter",
                "grocery store shelf",
                "behind the grocery counter",
                "grocery store counter"
            ]
        },
        "Dorm for Oak Hill College": {
            "garden": [
                "dorm garden"
            ],
            "common room": [
                "common room sofa",
                "pool table",
                "common room table"
            ]
        },
        "Johnson Park": {
            "park": [
                "park garden"
            ]
        },
        "Ryan Park's apartment": {
            "bathroom": [
                "shower",
                "bathroom sink",
                "toilet"
            ],
            "main room": [
                "bed",
                "cooking area",
                "kitchen sink",
                "refrigerator",
                "closet",
                "computer desk"
            ]
        },
        "Giorgio Rossi's apartment": {
            "bathroom": [
                "shower",
                "bathroom sink",
                "toilet"
            ],
            "main room": [
                "bed",
                "desk",
                "blackboard",
                "cooking area",
                "kitchen sink",
                "closet",
                "refrigerator"
            ]
        },
        "Carlos Gomez's apartment": {
            "main room": [
                "desk",
                "bed"
            ],
            "bathroom": []
        }
    }
}
```



## 2. 总结

`MemoryTree` 类是生成型代理的空间记忆模块，使用树形结构管理代理的空间记忆。它提供了丰富的方法来打印树形结构、保存和加载数据，以及获取代理可访问的区域和游戏对象的摘要字符串。这个模块在生成型代理的空间定位和行为管理中起着关键作用。
