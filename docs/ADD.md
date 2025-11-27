# Oron System Architecture Definition (v1.1.1)



Document ID: OUR-ADD-011-1

Version: 1.1.1 (Toolchain Evolution)

Date: 2025-11-27

Status: KERNEL / CONSTITUTION

Changelog:

- **v1.1.1:** 引入 **Global CLI Manager (全局命令行管理)** 概念。将 Layer 3 从单一脚本重构为模块化工具链，支持全局调用、咒语库管理（Spellbook）及上下文注入器（Injector）的解耦。
- **v1.1.0:** 引入 Architect (辅助构思模块)。
- **v1.0.1:** 确立 WGC 协议与 Conductor 核心。

------



## 1. 思路层：设计哲学 (Design Philosophy)





### 1.1 核心目标 (Objective)



Oron 旨在解决单一 LLM 在处理复杂、长周期软件工程项目时面临的四大物理瓶颈：

1. **Context Window Decay（上下文衰减）：** 随着对话变长，模型“变笨”。
2. **Context Air-Gap（上下文真空）：** 架构师（Conductor）不需要看每一行代码，而执行者（Worker）只需要看当前任务相关的代码。
3. **IO Fatigue（交互疲劳）：** 手工在不同上下文之间搬运数据、查找 Prompt 的成本过高（**v1.1.1 重点解决对象**）。
4. **Output Overload（输出过载）：** 单次任务粒度过大导致 Worker 注意力分散。



### 1.2 实现思路 (Implementation Strategy)



我们采用 **“二元分治 + 原子化派发 + 全局工具桥接”** 的架构：

- **大脑与手脚分离：** 将“长期记忆与规划”（Conductor）与“短期执行与编码”（Worker）物理隔离。
- **Atomic Dispatch (原子化派发)：** 遵循 **WGC 协议**。
- **状态即真理：** 项目进度完全由 Conductor 维护的 YAML 状态机决定。
- **Global Tooling (全局工具化)：** 使用系统级 CLI (`oron` 命令) 接管所有 I/O 操作，包括项目冷启动时的 Prompt 注入和开发过程中的代码上下文提取。

------



## 2. 架构内容层：系统拓扑 (System Topology)



本系统核心由三层组成。在 v1.1.1 中，**Layer 3 发生了结构性裂变**。



### [Optional] Layer 0: The Architect (扩展：构思助手)



- **定义：** 独立的 Prompt 模块 (`Architect_v1.1`)，存储于工具链的 `templates` 库中。
- **职责：** 需求清洗与结构化，生成《项目蓝图》(Blueprint)。



### 2.1 Layer 1: The Kernel (内核：架构定义)



- **定义：** 即本文档。
- **职责：** 定义数据流向、角色边界及物理约束。



### 2.2 Layer 2: The Core (核心：指挥家)



- **定义：** 注入给 Conductor 模型的 System Prompt (`Conductor_v1.0.1`)，存储于工具链的 `templates` 库中。
- **职责：** State Machine Owner（状态维护）、Traffic Controller（流量控制）、CLI Generator（指令生成）。



### 2.3 Layer 3: The Interface (交互层：全局工具链)



- **定义：** 部署于宿主操作系统 PATH 中的模块化 Python 工具包 (Global Oron Manager)。
- **职责：** 消除人类与 LLM 之间的物理操作摩擦。
- **模块组成：**
  - **The Manager (CLI Menu):** `manager.py`。交互入口，负责路由用户请求（获取咒语 vs 执行注入）。
  - **The Spellbook (咒语库):** 负责读取静态资源（MD 文档）并自动写入剪贴板，解决“冷启动寻找文档”的痛点。
  - **The Injector (注入器):** 原 `oron.py` 的核心逻辑。负责在**当前工作目录 (CWD)** 下执行上下文抓取和 Prompt 组装。

------



## 3. 关键机制说明 (Key Mechanisms)





### 3.1 状态机流转 (State Machine)



*(保持不变：PLANNING -> FISSION -> DISPATCH -> WAITING -> VERIFYING -> LOCKED)*



### 3.2 智能上下文注入 (Smart Context Injection)



- **Scope Awareness (作用域感知):** Injector 模块自动识别终端当前的运行目录作为项目根目录，无需物理移动脚本文件。
- **Mode Selection:** 依旧区分 Reading Mode 与 Creation Mode。



### 3.3 Worker 粒度控制协议 (WGC Protocol)



*(保持不变：The Rule of Three)*



### 3.4 零摩擦启动协议 (Zero-Friction Bootstrapping) [New]



- **原理：** 所有的 System Prompts (Kernel/Core/Architect) 被视为**只读资源**，托管在全局工具链中。
- **操作流：** 用户无需打开 Markdown 文件复制文本。通过 CLI 菜单选择对应角色，系统自动完成读取与剪贴板写入。

------



## 4. 快速开始 (Quick Start Guide)





### Step 0: 环境部署 (One-time Setup)



- 将 Oron 工具包 (`manager.py` 及 `modules/`, `templates/`) 放置于系统目录（如 `~/tools/oron`）。
- 配置系统环境变量或 Alias，使得在终端任意位置输入 `oron` 即可唤醒菜单。



### Step 1: 项目构思与初始化



- 打开终端，输入 `oron`。
- **场景 A (需要构思):** 选择菜单 `[1] Copy Architect Prompt` -> 粘贴给 LLM -> 生成蓝图。
- **场景 B (直接开始):** 选择菜单 `[2] Copy Conductor Prompt` -> 粘贴给 LLM (推荐新窗口) -> 激活 Conductor。



### Step 2: 循环作业 (The Loop)



- **Conductor:** 输出指令 (如 `oron -r src/main.py`)。
- **User:**
  1. 在项目终端粘贴并运行该指令（将直接调用全局 Injector 模块）。
  2. System 提示 `Context copied to clipboard`。
  3. 粘贴给 Worker -> 获取代码 -> 验证。

------



## 5. 迭代维护指南 (Maintenance)



- **Templates 维护：** 修改 `templates/` 目录下的 `.md` 文件即可更新所有未来项目的 Prompt 版本，无需逐个项目更新。
- **Modules 维护：**
  - `manager.py`: 负责菜单逻辑和路由。
  - `injector.py`: 负责文件读取和 Prompt 拼接逻辑（原 Adapter 逻辑）。
  - `spellbook.py`: 负责资源读取和剪贴板操作。