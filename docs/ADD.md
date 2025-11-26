- # Oron System Architecture Definition (v1.1.0)

  

  **Document ID:** OUR-ADD-011 **Version:** 1.1.0 (Extension) **Date:** 2025-11-27 **Status:** KERNEL / CONSTITUTION **Changelog:** 在保持 v1.0.1 核心架构（Conductor/Adapter/WGC）完全不变的基础上，引入可选的 **Architect (辅助构思模块)** 以优化项目冷启动体验。

  ------

  

  ## 1. 思路层：设计哲学 (Design Philosophy)

  

  

  ### 1.1 核心目标 (Objective)

  

  Oron 旨在解决单一 LLM 在处理复杂、长周期软件工程项目时面临的四大物理瓶颈：

  1. **Context Window Decay（上下文衰减）：** 随着对话变长，模型“变笨”。
  2. **Context Air-Gap（上下文真空）：** 架构师（Conductor）不需要看每一行代码，而执行者（Worker）只需要看当前任务相关的代码。
  3. **IO Fatigue（交互疲劳）：** 手工在不同上下文之间搬运数据的成本过高。
  4. **Output Overload（输出过载）：** 单次任务粒度过大导致 Worker 注意力分散、代码质量下降及产生幻觉。

  

  ### 1.2 实现思路 (Implementation Strategy)

  

  我们采用 **“二元分治 + 原子化派发 + 工具桥接”** 的架构：

  - **大脑与手脚分离：** 将“长期记忆与规划”（Conductor）与“短期执行与编码”（Worker）物理隔离。
  - **Atomic Dispatch (原子化派发)：** 遵循 **WGC 协议**，将逻辑步骤拆解为物理微任务。
  - **状态即真理：** 项目进度完全由 Conductor 维护的 YAML 状态机决定。
  - **工具化 I/O：** 通过本地脚本（Middleware）自动化完成上下文的提取和注入。

  ------

  

  ## 2. 架构内容层：系统拓扑 (System Topology)

  

  本系统核心由三层组成（Kernel/Core/Adapter）。**Architect 为可选的第 0 层辅助扩展。**

  

  ### [Optional] Layer 0: The Architect (扩展：构思助手)

  

  - **定义：** 独立的 Prompt 模块 (`Architect_v1.1`)。
  - **职责：** **需求清洗与结构化**。通过对话引导用户，生成符合 Conductor 解析标准的《项目蓝图》(Blueprint)。
  - **依赖关系：** **无强依赖**。系统可在无 Architect 的情况下通过用户自然语言直接启动。

  

  ### 2.1 Layer 1: The Kernel (内核：架构定义)

  

  - **定义：** 即本文档。
  - **职责：** 定义数据流向、角色边界、状态流转规则及物理约束（Physical Constraints）。

  

  ### 2.2 Layer 2: The Core (核心：指挥家)

  

  - **定义：** 注入给 Conductor 模型的 System Prompt (`Conductor_v1.0.1`)。
  - **职责：**
    - **State Machine Owner：** 维护项目状态（Planning -> Dispatch -> Verify）。
    - **Traffic Controller：** 强制执行 WGC 协议，在生成指令前预估 Worker 负载。
    - **CLI Generator：** 生成符合 Middleware 语法的指令。
  - **兼容性：** 既接受自然语言输入（模糊目标），也接受 Architect 生成的蓝图（精确目标）。

  

  ### 2.3 Layer 3: The Adapter (适配件：中间件脚本)

  

  - **定义：** 本地运行的 `oron.py` (Python Script)。
  - **职责：** 物理 I/O 执行者。
    - **Context Gathering：** 区分读取模式与创建模式。
    - **Prompt Injection：** 自动写入剪贴板。

  ------

  

  ## 3. 关键机制说明 (Key Mechanisms)

  

  

  ### 3.1 状态机流转与裂变 (State Machine & Fission)

  

  Conductor 必须严格遵守以下流转：

  - **PLANNING (规划态)：** 分析需求。若输入为《蓝图》，则直接转化为执行队列；若为自然语言，则先进行拆解。
  - **FISSION CHECK (裂变判定)：** [Core Rule] 判定 Step 是否超过 WGC 阈值。若超过，必须拆解为 Task 1.1, 1.2...
  - **DISPATCH_READY (指令态)：** 输出 Adapter 调用指令。
  - **WAITING_EXECUTION (挂起态)：** 等待 Worker 结果。
  - **VERIFYING (验收态)：** 用户反馈 VERIFIED 或 FAILED。
  - **LOCKED_DONE (归档态)：** 更新依赖图谱。

  

  ### 3.2 智能上下文注入 (Smart Context Injection)

  

  - **Reading Mode (读取模式)：** 仅读取已存在的参考文件。
  - **Creation Mode (创建模式)：** 针对 Create 任务，不读取目标文件，防止 "Missing File" 报错。

  

  ### 3.3 Worker 粒度控制协议 (WGC Protocol)

  

  **The Rule of Three (三原则约束)：** 任何一次 Dispatch 指令，不得超过：

  1. **文件数量：** 最多 3 个。
  2. **功能点：** 仅 1 个核心逻辑。
  3. **行数直觉：** 预估 < 150 行。

  ------

  

  ## 4. 快速开始 (Quick Start Guide)

  

  

  ### Step 0: 环境准备

  

  - 在项目根目录创建 `oron.py`。
  - 安装依赖：`pip install pyperclip`。

  

  ### Step 1: 项目构思（选择一种路径）

  

  

  #### 路径 A：标准启动 (Direct Mode)

  

  - *适用场景：简单项目，或用户心中已有清晰架构。*
  - 直接进入 Step 2。

  

  #### 路径 B：辅助启动 (Architect Mode)

  

  - *适用场景：复杂项目，需要梳理需求和技术栈。*
  - 向 LLM 发送 **[Architect Prompt]**。
  - 通过对话确认需求，获得 Markdown 格式的 **《项目蓝图》**。

  

  ### Step 2: 激活 Conductor (核心启动)

  

  - 向 LLM (推荐新窗口) 发送 **[Conductor Prompt]**。
  - **初始化输入：**
    - 若走路径 A：直接输入 "项目名：X，我想做一个..."
    - 若走路径 B：直接粘贴 **《项目蓝图》**。

  

  ### Step 3: 循环作业 (The Loop)

  

  - **Conductor:** 输出 CLI 指令 (`python oron.py ...`).
  - **User:** 运行命令 -> 粘贴给 Worker -> 验证代码 -> 反馈结果。

  ------

  

  ## 5. 迭代维护指南 (Maintenance)

  

  - **修改 Kernel (本文档)：** 定义新的物理约束。
  - **更新 Core (Conductor)：** 这是系统的心脏。修改需谨慎，确保不破坏 WGC 逻辑。
  - **更新 Architect (可选)：** 优化构思引导逻辑。Architect 的更新**不需要**同步更新 Conductor。
  - **更新 Adapter (代码)：** 优化 `oron.py` 的 I/O 兼容性。