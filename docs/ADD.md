# Oron System Architecture Definition (v1.0.1)



- **Document ID:** OUR-ADD-001
- **Version:** 1.0.1 (Optimized)
- **Date:** 2025-11-26
- **Status:** KERNEL / CONSTITUTION
- **Changelog:** 引入 Worker 粒度控制 (WGC) 与原子化派发原则，解决 Worker 过载问题。

------



## 1. 思路层：设计哲学 (Design Philosophy)





### 1.1 核心目标 (Objective)



Oron 旨在解决单一 LLM 在处理复杂、长周期软件工程项目时面临的**四大物理瓶颈**：

1. **Context Window Decay（上下文衰减）：** 随着对话变长，模型“变笨”。
2. **Context Air-Gap（上下文真空）：** 架构师（Conductor）不需要看每一行代码，而执行者（Worker）只需要看当前任务相关的代码。
3. **IO Fatigue（交互疲劳）：** 手工在不同上下文之间搬运数据的成本过高。
4. **Output Overload（输出过载）：** *[New]* 单次任务粒度过大导致 Worker 注意力分散、代码质量下降及产生幻觉。



### 1.2 实现思路 (Implementation Strategy)



我们采用 **“二元分治 + 原子化派发 + 工具桥接”** 的架构：

- **大脑与手脚分离：** 将“长期记忆与规划”（Conductor）与“短期执行与编码”（Worker）物理隔离。
- **Atomic Dispatch (原子化派发)：** *[New]* 宁可多跑几轮，不可一轮撑死。遵循 WGC 协议，将逻辑步骤拆解为物理微任务。
- **状态即真理：** 项目进度由 Conductor 维护的 YAML 状态机决定。
- **工具化 I/O：** 通过本地脚本（Middleware）自动化完成上下文的提取和注入。

------



## 2. 架构内容层：系统拓扑 (System Topology)



本系统由三个相互依赖的层级组成。Kernel 约束 Core，Core 驱动 Adapter。



### 2.1 Layer 1: The Kernel (内核：架构定义)



- **定义：** 即本文档。
- **职责：** 定义数据流向、角色边界、状态流转规则及物理约束（Physical Constraints）。
- **依赖关系：** 它是系统的“静态真理”。严禁 Core 生成违背本层定义的超长指令。



### 2.2 Layer 2: The Core (核心：初始化咒语)



- **定义：** 注入给 Conductor 模型的 System Prompt。
- **职责：**
  - 维护项目状态机（Planning -> Dispatch -> Verify）。
  - **Traffic Controller (流量控制)：** *[New]* 在生成指令前，必须预估 Worker 的 Token 负载，执行微任务拆分。
  - 生成符合 Middleware 语法的 CLI 指令。



### 2.3 Layer 3: The Adapter (适配件：中间件脚本)



- **定义：** 本地运行的 `ouro.py` (Python Script)。
- **职责：**
  - **Context Gathering:** 响应 Core 指令读取文件。*[Update]* 需区分“读取模式”与“创建模式”，避免对不存在的新文件报错。
  - **Prompt Injection:** 将代码包裹在 Markdown 格式中，自动写入剪贴板。
- **依赖关系：** 它是 Core 的物理延伸，不包含业务逻辑，只负责 I/O 操作。

------



## 3. 关键机制说明 (Key Mechanisms)





### 3.1 状态机流转与裂变 (State Machine & Fission)



Conductor 必须严格遵守以下流转，并引入**微任务规划**：

1. **PLANNING (规划态):** 分析需求，制定逻辑步骤。
2. **FISSION CHECK (裂变判定):** *[New]* 判定当前 Step 是否超过“WGC 协议”阈值。若超过，必须将 Step 拆解为 Task 1.1, Task 1.2 等连续的微任务。
3. **DISPATCH_READY (指令态):** 输出 Adapter 调用指令。对于“创建新文件”的任务，不得将文件名作为读取参数传入，以免触发 Adapter 报错。
4. **WAITING_EXECUTION (挂起态):** 等待用户完成 Worker 窗口的工作。
5. **VERIFYING (验收态):** 用户反馈 VERIFIED 或 FAILED。
6. **LOCKED_DONE (归档态):** 更新依赖图谱，进入下一轮 Planning。



### 3.2 智能上下文注入 (Smart Context Injection)



- **原则：** Worker 是无状态且“健忘”的。
- **修正机制：**
  - **Reading Mode (读取模式):** 仅读取已存在的、对当前任务至关重要的参考文件。
  - **Creation Mode (创建模式):** *[New]* 当任务目标是 Create 时，Adapter 不应尝试从磁盘读取该目标文件（防止 `!!! MISSING FILE !!!` 噪音），而是直接提示 Worker 进行全新创作。



### 3.3 接口签名防腐层 (Interface Signature ACL)



Conductor 的内存（YAML）中只保存接口签名，不保存实现细节。

- Keep: `class Auth(user, pass) -> token`
- Discard: 具体实现代码（100+ lines）



### 3.4 Worker 粒度控制协议 (WGC Protocol) *[New]*



为了保证 Worker 输出质量，Conductor 在 DISPATCH 阶段必须强制执行 **SRP (Single Responsibility Physicalization)**。 **The Rule of Three (三原则约束):** 任何一次 Dispatch 指令，**不得**超过以下界限之一：

1. **文件数量限制：** 最多触碰/创建 **3 个** 文件。
2. **功能点限制：** 仅实现 **1 个** 核心逻辑（例如：只写数据层，不写视图层）。
3. **行数直觉：** 预估 Worker 输出代码总行数不超过 **150 行**。

如果逻辑步骤超出上述限制，必须强制触发 **Fission (裂变)**，将其拆分为多次 Dispatch 循环。

------



## 4. 快速开始 (Quick Start Guide)





### Step 0: 环境准备



- 在项目根目录创建 `ouro.py`。
- 安装依赖：`pip install pyperclip`。



### Step 1: 激活 Conductor (大脑)



- 打开 LLM 会话，发送 `[Core Spell v1.0.1]`。
- 输入项目目标。



### Step 2: 循环作业 (The Loop)



- **指令接收：** Conductor 输出 `python ouro.py ...` (遵循 WGC 协议，短小精悍)。
- **本地执行：** 运行命令。注意观察是否为“多轮微任务”。
- **Worker 执行：** 粘贴给 Worker。
- **代码同步 & 验证：** 复制回本地，验证后回复 Conductor。

------



## 5. 迭代维护指南 (Maintenance)



- **修改 Kernel (本文档):** 定义新的物理约束或流转规则。
- **更新 Core (咒语):** 修改 Prompt 以使其理解并遵守 WGC 协议和裂变规则。
- **更新 Adapter (代码):** 优化 `ouro.py` 以消除 Missing File 噪音，支持更灵活的文件操作。