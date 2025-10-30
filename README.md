# 坦克大战 Roguelike Battle

## 游戏简介

《坦克大战 Roguelike Battle》是一款结合了经典坦克战斗与Roguelike元素的动作游戏。玩家将操控一辆坦克在随机生成的地图中与敌人战斗，通过击败敌人获得经验升级，选择各种功能卡片来增强能力，体验不断成长的快感。

## 游戏特色

### 🎯 核心玩法
- **Roguelike元素**：每次游戏都是全新体验，随机生成的敌人和卡片选择
- **升级系统**：击败敌人获得经验，升级后选择强化卡片
- **多样化敌人**：普通敌人、狙击手、追击者、强大Boss等多种敌人类型
- **物理碰撞**：真实的墙体碰撞和子弹物理效果

### 🛡️ 能力系统
- **属性提升**：伤害、射速、移动速度、生命值、暴击等
- **特殊能力**：穿透射击、散射、追踪子弹、吸血效果等
- **道具系统**：炸弹等特殊道具，提供战术选择

### 🎮 游戏模式
- **主菜单**：简洁的界面设计
- **游戏进行**：实时战斗与策略选择
- **暂停界面**：查看详细属性状态
- **控制台**：开发者调试功能

## 操作说明

### 键盘控制
| 操作 | 按键 |
|------|------|
| 移动 | W/A/S/D |
| 射击 | 方向键(↑↓←→) |
| 暂停游戏 | P |
| 选择卡片 | Q |
| 使用道具 | 空格键 |
| 打开控制台 | ` |
| 全屏切换 | F |
| 音量调整 | +/- |
| 重新开始 | R |
| 退出游戏 | ESC |

### 移动设备控制
- **虚拟摇杆**：左侧区域控制移动
- **射击按钮**：右侧四个方向按钮控制射击

## 游戏机制

### 升级系统
- 击败敌人获得分数，积累足够分数后升级
- 每升2-5级获得一次选择卡片的机会
- 升级同时提升最大生命值和基础伤害

### 卡片系统
游戏包含多种功能卡片，分为不同等级：

#### 属性类卡片
- **吸血+2%**：增加吸血比例
- **暴击几率+5%**：提高暴击概率
- **生命值+100**：增加最大生命值
- **射速+0.1**：提高射击速度
- **移动速度+10%**：提升移动能力
- **子弹速度+0.5**：增加子弹飞行速度
- **射程+15/50**：扩大攻击范围
- **伤害+20%**：提升伤害输出

#### 功能类卡片
- **牛奶**：降低伤害但大幅提高射速
- **穿透**：子弹可以穿透多个目标
- **钻孔机**：降低伤害和射速，但造成持续伤害
- **散射器**：一次发射多颗子弹
- **意识**：子弹具备追踪能力
- **石头**：大幅增加伤害但降低移动速度

#### 道具类卡片
- **炸弹**：获得炸弹道具，可造成范围伤害

### 敌人类型
1. **普通敌人**：基础属性均衡
2. **狙击手**：远程高伤害，生命值较高
3. **追击者**：移动速度快，攻击力中等
4. **Boss**：超强生命值和伤害，特殊攻击模式

## 系统要求

### 最低配置
- **操作系统**：Windows 7/10/11, Android, iOS
- **处理器**：1.5 GHz
- **内存**：2 GB RAM
- **显卡**：支持OpenGL 2.0
- **存储空间**：100 MB可用空间

### 推荐配置
- **操作系统**：Windows 10/11
- **处理器**：2.0 GHz双核
- **内存**：4 GB RAM
- **显卡**：支持OpenGL 3.0
- **存储空间**：100 MB可用空间

## 安装说明

1. 下载游戏文件
2. 确保安装Python 3.8或更高版本
3. 安装Pygame库：`pip install pygame`
4. 运行`main.py`开始游戏

## 开发者信息

- **开发团队**：冰之龙晶
- **版本**：1.0
- **联系方式**：3457534204@qq.com

## 故障排除

### 常见问题
1. **游戏无法启动**
   - 检查Python和Pygame是否正确安装
   - 确保所有游戏文件完整

2. **音效问题**
   - 检查系统音量设置
   - 确认音频驱动正常工作

3. **性能问题**
   - 关闭其他应用程序释放内存
   - 降低游戏分辨率

## 更新日志

### v1.0
- 初始版本发布
- 基础游戏功能实现
- 卡片系统和敌人AI

---

# Roguelike Battle - Tank Game

## Game Introduction

"Roguelike Battle" is an action game that combines classic tank combat with Roguelike elements. Players control a tank to battle enemies in randomly generated maps, gain experience by defeating enemies, level up, and choose various function cards to enhance abilities, experiencing the thrill of continuous growth.

## Game Features

### 🎯 Core Gameplay
- **Roguelike Elements**: Each game is a new experience with randomly generated enemies and card choices
- **Leveling System**: Gain experience by defeating enemies, choose enhancement cards upon leveling up
- **Diverse Enemies**: Multiple enemy types including regular enemies, snipers, chasers, and powerful bosses
- **Physics Collision**: Realistic wall collisions and bullet physics

### 🛡️ Ability System
- **Attribute Enhancement**: Damage, fire rate, movement speed, health, critical hits, etc.
- **Special Abilities**: Penetrating shots, scattering, homing bullets, life steal effects, etc.
- **Item System**: Special items like bombs providing tactical choices

### 🎮 Game Modes
- **Main Menu**: Clean interface design
- **Gameplay**: Real-time combat and strategic choices
- **Pause Interface**: View detailed attribute status
- **Console**: Developer debugging functions

## Controls

### Keyboard Controls
| Action | Key |
|--------|-----|
| Movement | W/A/S/D |
| Shooting | Arrow Keys(↑↓←→) |
| Pause Game | P |
| Select Card | Q |
| Use Item | Spacebar |
| Open Console | ` |
| Toggle Fullscreen | F |
| Volume Adjustment | +/- |
| Restart | R |
| Exit Game | ESC |

### Mobile Controls
- **Virtual Joystick**: Left area for movement control
- **Shooting Buttons**: Four directional buttons on the right for shooting

## Game Mechanics

### Leveling System
- Gain score by defeating enemies, level up after accumulating enough score
- Get card selection opportunities every 2-5 levels
- Increase maximum health and base damage when leveling up

### Card System
The game includes various function cards divided into different levels:

#### Attribute Cards
- **Leech+2%**: Increase life steal ratio
- **Critical Chance+5%**: Improve critical hit probability
- **Health+100**: Increase maximum health
- **Shoot Speed+0.1**: Improve firing speed
- **Speed+10%**: Enhance movement ability
- **Bullet Speed+0.5**: Increase bullet flight speed
- **Range+15/50**: Expand attack range
- **Damage+20%**: Boost damage output

#### Function Cards
- **Milk**: Reduce damage but significantly increase fire rate
- **Penetrate**: Bullets can penetrate multiple targets
- **Borer**: Reduce damage and fire rate but cause sustained damage
- **Scatterer**: Fire multiple bullets at once
- **Consciousness**: Bullets have homing capability
- **Stone**: Greatly increase damage but reduce movement speed

#### Item Cards
- **Boom**: Obtain bomb item that can cause area damage

### Enemy Types
1. **Regular Enemies**: Balanced basic attributes
2. **Snipers**: Long-range high damage, higher health
3. **Chasers**: Fast movement speed, medium attack power
4. **Boss**: Extremely high health and damage, special attack patterns

## System Requirements

### Minimum Requirements
- **OS**: Windows 7/10/11, Android, iOS
- **Processor**: 1.5 GHz
- **Memory**: 2 GB RAM
- **Graphics**: OpenGL 2.0 support
- **Storage**: 100 MB available space

### Recommended Requirements
- **OS**: Windows 10/11
- **Processor**: 2.0 GHz dual-core
- **Memory**: 4 GB RAM
- **Graphics**: OpenGL 3.0 support
- **Storage**: 100 MB available space

## Installation Instructions

1. Download game files
2. Ensure Python 3.8 or higher is installed
3. Install Pygame library: `pip install pygame`
4. Run `main.py` to start the game

## Developer Information

- **Development Team**: 冰之龙晶
- **Version**: 1.0
- **Contact**: 3457534204@qq.com

## Troubleshooting

### Common Issues
1. **Game Won't Start**
   - Check if Python and Pygame are properly installed
   - Ensure all game files are complete

2. **Audio Issues**
   - Check system volume settings
   - Confirm audio drivers are working properly

3. **Performance Issues**
   - Close other applications to free up memory
   - Reduce game resolution

## Changelog

### v1.0
- Initial version release
- Basic game functions implemented
- Card system and enemy AI

---


**Enjoy the game! 祝您游戏愉快!**
