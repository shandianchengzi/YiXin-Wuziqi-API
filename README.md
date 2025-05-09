# YiXin-Wuziqi-API

这是一个用于调用弈心引擎进行五子棋对战的 Python API，支持网页版接口和本地运行，旨在为五子棋游戏提供强大的 AI 对手。

## 仓库介绍

本项目提供了一个简单的接口，用于与强大的弈心五子棋 AI 进行交互。通过这个 API，你可以轻松地在自己的五子棋项目中集成弈心 AI，提升游戏的智能程度和趣味性。该项目的开发初衷是为了满足对高性能五子棋 AI 的需求，并提供一个易于使用的接口供其他开发者集成和使用。

## 使用方法

### 环境准备

在使用本 API 之前，请确保你的环境中已经安装了 Python（推荐 3.9 或更高版本）。

### 文件结构

```
YiXin-Wuziqi-API/
├── LICENSE
├── README.md
├── Yixin2018.exe
├── YiXinGame.py
└── YiXinGame_Gomoku.py
```

### 运行方式

#### 本地运行

  1. 将本仓库克隆至本地。
  2. 在命令行中进入项目目录。
  3. 运行 `python YiXinGame.py`。

#### 通过网页版接口运行

  1. 将本仓库克隆至本地。
  2. 在命令行中进入项目目录。
  3. 修改 `YiXinGame_Gomoku.py` 开头的各种变量，或者自行调整相应接口，使其适配你的 Gomoku 网页请求。
  4. 运行 `python YiXinGame_Gomoku.py`。
  5. 通过网页版接口自动使用弈心引擎进行对战。

### 代码示例

以下是一个简单的代码示例，展示如何使用本 API 进行五子棋对战：

```python
from YiXinGame import Game, start_game_test
from YiXinGame_Gomoku import start_game

mod = Game()
start_game_test(mod) # 终端直接运行五子棋程序
start_game(mod) # 通过网页版接口运行五子棋程序
```

更多开发详情，请参考 [项目博客](https://shandianchengzi.blog.csdn.net/article/details/147818197)。

## 文件说明

  * `Yixin2018.exe` ：弈心引擎的可执行文件。
  * `YiXinGame.py` ：提供了一个简单的接口，用于调用弈心引擎进行五子棋对战。
  * `YiXinGame_Gomoku.py` ：实现了与 Gomoku 棋盘的集成，支持通过网页版接口进行对战。

## 许可证

本项目采用 [GPLv3 License](LICENSE) 许可证。请在使用本项目时遵守许可证的规定。

## 项目博客

更多关于本项目的详细信息，请访问 [项目博客](https://shandianchengzi.blog.csdn.net/article/details/147818197)。