# 肉鸽弹幕射击（roguelikeTankShootingGame）

## 中文说明

项目简介

这是一个基于 Pygame 的简单坦克大战游戏（教学/练习项目）。项目包含玩家坦克、敌方坦克、子弹、墙体、爆炸效果、道具等基本要素。目标是保持代码结构清晰并便于扩展。

主要功能

- 玩家控制坦克移动与射击。
- 敌方坦克具有基本行动/射击逻辑。
- 子弹、爆炸、道具等精灵由单独类管理。
- 使用 Pygame 的精灵组进行碰撞与渲染管理。
- 控制台可以输入指令进行卡牌获取等。
- roguelike 卡牌选择与角色成长系统。

运行要求

- Python 3.7+
- Windows（文档中的命令以 PowerShell 为例）
- Pygame

安装依赖（推荐步骤）

1. 可选：创建并激活虚拟环境（PowerShell）

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. 安装依赖

```powershell
pip install -r requirements.txt
```

快速运行

在激活虚拟环境后，运行：

```powershell
python main.py
```

项目结构（关键文件/目录）

- `main.py` - 程序入口，游戏主循环
- `variable.py` - 存放全局变量（注意：尽量减少可变全局，见下方注意事项）
- `sprites/` - 精灵类目录（已将各精灵类封装为单独文件）
  - `tank.py` - 坦克类（包含玩家与敌方坦克逻辑）
  - `bullet.py` - 子弹类
  - `wall.py` - 墙体类
  - `timer.py` - 计时器/定时类
  - `floating_text.py` - 浮动文本/提示
  - `function_card.py` - 功能卡/道具卡类（若有）
- `spirit/`、`image/`、`sound/` 等资源目录
- 其它模块：`function.py`、`key_event.py`、`prop_functions.py`、`restart.py`、`sprites_init.py`、`console.py` 等

精灵封装与变量处理说明

- 为提高可维护性，项目将每个主要精灵类拆分成单独的 `.py` 文件并放入 `sprites/` 目录（保留原注释）。
- 拆分时请注意：
  - 尽量避免在类内直接引用未导入的全局变量。若需要共享变量，建议通过构造函数传入（例如：屏幕对象、配置、精灵组或变量容器）。
  - 若确实需要访问 `variable.py` 中的全局配置，请在文件顶部显式导入：`from variable import SOME_VAR`，并谨慎修改可变对象。
  - 对于相互引用的精灵（例如 `Tank` 需要创建 `Bullet`），避免循环导入：可在类型注解中使用字符串或在方法体内局部导入（例如：`from sprites.bullet import Bullet` 放在函数内部）。
- 保留原注释以便保留逻辑意图。

常见问题与调试建议

- 如果程序因循环导入（ImportError）崩溃，检查模块间的相互导入，考虑将共享类型导入移到函数内或使用延迟导入。
- 渲染问题通常与图像路径或 Pygame 初始化顺序有关，确认 `pygame.init()` 在使用之前已调用。
- 若碰撞检测或精灵行为异常，先检查精灵的 rect（边界）和更新（`update`）实现。

许可证与贡献

此项目为个人/教学项目，代码可自由学习参考；若计划公开发布或商用，请联系原作者并遵守相应许可。


---

## English (Translation)

Project Overview

This is a simple Tank Battle game built with Pygame (learning/exercise project). It includes player tanks, enemy tanks, bullets, walls, explosion effects and power-ups. The intent is to keep the codebase clear and easy to extend.

Features

- Player-controlled tank movement and shooting.
- Basic enemy tank behavior and shooting.
- Bullets, explosions, and items managed by separate sprite classes.
- Use Pygame sprite groups for collision and rendering.
- Console for inputting commands to control card acquisition, etc.
- Roguelike card selection and character progression system.

Requirements

- Python 3.7+
- Windows (the commands below use PowerShell)
- Pygame

Install dependencies (recommended)

1. Optional: create and activate a virtual environment (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

Run

```powershell
python main.py
```

Project layout (key files/dirs)

- `main.py` - entry point and game loop
- `variable.py` - global variables (try to minimize mutable globals; see notes)
- `sprites/` - sprite classes (moved to individual files)
  - `tank.py` - Tank class (player & enemy)
  - `bullet.py` - Bullet class
  - `wall.py` - Wall class
  - `timer.py` - Timer class
  - `floating_text.py` - Floating text / HUD
  - `function_card.py` - Function/power-up card class (if present)
- resource dirs: `spirit/`, `image/`, `sound/`
- other modules: `function.py`, `key_event.py`, `prop_functions.py`, `restart.py`, `sprites_init.py`, `console.py`, etc.

Sprites refactor & variable handling notes

- Each major sprite class has been split into its own `.py` file under `sprites/` (original comments preserved).
- Recommendations when refactoring:
  - Avoid directly referencing global variables inside class bodies. Pass required objects via constructor (screen, config, groups, or a variables container).
  - If you must read from `variable.py`, import explicitly at the top: `from variable import SOME_VAR`, and be careful when mutating shared objects.
  - To prevent circular imports (e.g. `Tank` creating `Bullet`), use local imports within methods or type annotations as strings.
- Original comments are preserved to retain intent.

Troubleshooting

- ImportError due to circular imports: move imports into functions or centralize shared types.
- Rendering issues: ensure `pygame.init()` runs before creating surfaces.
- Collision/behavior bugs: inspect sprite rects and `update()` implementations.

License & Contribution

This is a personal/teaching project. Code may be used for learning and reference; for public or commercial use contact the original author and follow licensing requirements.
