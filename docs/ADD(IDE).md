# Oron System Architecture Definition (v2.2.0)

Document ID: OUR-ADD-022-0
Version: 2.2.0 (Semi-Automated Conductor Workflow)
Date: 2025-12-01
Status: KERNEL / CONSTITUTION

Changelog:
- **v2.2.0:** **优化 Conductor 工作流**。明确 Conductor AI 可利用现代 IDE 插件（如 Gemini, Copilot）的文件系统能力，**直接读取并请求修改 `oron.state.yml`**。用户角色从“手动复制粘贴状态文件”简化为“**审批 AI 提出的文件变更**”。
- **v2.1.0:** 架构重大修正。明确 Oron 是一个“工作流协议 + 辅助工具集”，人类用户是协议的执行者。
- **v2.0.1:** (Conceptual) 确立 "AI 注意力管理" 为核心设计哲学。
- **v2.0.0:** (Conceptual) 引入基于 IDE 的 "AI 团队协作" 模型及 `oron.state.yml`。

------

## 1. 思路层：设计哲学 (Design Philosophy)

### 1.1 核心哲学：AI 注意力管理 (Core Philosophy: AI Attention Management)

Oron v2 的核心哲学依然是**AI 注意力管理**。我们承认，无论是 Conductor 还是 Worker，其本质都是在一个独立的、有上下文限制的 AI 对话中运行。Oron 的目标就是通过一套精巧的**协议和工作流**，来帮助**人类用户**高效地引导和管理不同 AI Agent 的注意力焦点。

- **Conductor (AI 项目经理):** 聚焦于**宏观的项目状态**。它通过 AI 插件的**原生文件系统能力**直接读取和提议修改 `oron.state.yml`，从而完成任务分解、调度和追踪。
- **Worker (AI 程序员):** 聚焦于**微观的代码实现**。它依赖**用户**提供的、经过 Oron 协议规范过的精确指令 (`order`) 和代码上下文，进行编码工作。

### 1.2 实现思路：以人为中心的 AI 协同协议 (Implementation: Human-centric AI Collaboration Protocol)

v2.2.0 架构进一步优化了以人为中心的协同协议，实现了 Conductor 环节的半自动化。

- **协议即规范 (Protocol as Specification):** Oron 的核心产出是一套关于如何组织 `oron.state.yml`、如何定义 `order`、以及人类如何在 Conductor 和 Worker 之间传递信息的工作流规范。
- **审批取代手动 (Approval over Manual I/O):** 在 Conductor 环节，用户通过审批 AI 提出的文件变更来更新项目状态，消除了手动复制粘贴的繁琐操作。
- **人类仍为桥梁 (Human Remains the Bridge):** 用户依然是连接 Conductor 和 Worker 两个独立AI会话的关键桥梁。
- **插件即助手 (Plugin as a Helper):** Oron Helper 插件的价值更加聚焦于为 Conductor->Worker 的“交接棒”过程提效。

------

## 2. 架构内容层：系统拓扑 (System Topology)

### 2.1 Layer 1: The Kernel (内核：Oron 协议)
- **定义：** 即本文档。它定义了 Oron 工作流的最高纲领。

### 2.2 Layer 2: The Agents (智能体：Prompt 定义)
- **定义：** 一系列存储于项目模板库中的 System Prompt `.md` 文件（如 `conductor.prompt.md`, `worker.prompt.md`）。
- **职责：** 用户在与 AI 交互时，负责将这些 Prompt 手动复制到各自的 AI 对话窗口，以“扮演”对应的角色。

### 2.3 Layer 3: The Interface (交互层：用户 + 辅助插件)
- **定义:** 系统的交互层由两部分构成：
    1.  **人类用户 (The User):** Oron 协议的执行者和审批者。
    2.  **Oron Helper (IDE 插件):** 一个功能有限但实用的辅助工具。
- **辅助插件 (Helper) 的核心功能:**
    - **State Viewer:** 在 IDE 侧边栏中，以更友好的 UI 可视化 `oron.state.yml` 的任务列表和状态。
    - **Prompt Assembler:** 在 State Viewer 中为每个任务提供 **[Copy Worker Prompt]** 按钮。点击后，插件会将 `order` 和相关代码**组装成一个完整的 Prompt 并复制到用户的剪贴板**。
    - **Quick File Navigator:** 提供文件链接，让用户可以快速跳转到任务所涉及的文件。

------

## 3. 关键机制说明 (Key Mechanisms)

### 3.1 半自动化的状态管理 (Semi-Automated State Management)

- **唯一真理来源:** `oron.state.yml` 是项目记忆的唯一载体。
- **交互流程 (Conductor 环节):**
    1.  **指令与授权:** 用户在 Conductor AI 对话中下达高级指令，并使用 AI 插件的原生语法（如 `@workspace` 或类似功能）授权其读取 `oron.state.yml` 文件。例如: `"Conductor, please break down the new feature requirements and update the plan. Here is the current state: @workspace /oron.state.yml"`。
    2.  **AI 处理与提议:** Conductor AI 读取并分析文件内容，然后通过插件功能**直接生成对 `oron.state.yml` 文件的修改提议**。
    3.  **用户审批:** IDE 会以 Diff 的形式向用户展示变更。用户审查后，**一键接受 (Accept)** 该变更，文件即被更新。

### 3.2 辅助的上下文交接 (Assisted Context Handoff)

- **剪贴板驱动:** 从 Conductor 到 Worker 的上下文传递（即 `order` 的传递）依然通过剪贴板完成，因为它们属于不同的 AI 会话。
- **Helper 提效:** Oron Helper 插件的**核心价值**在于，将“从YAML中找到并复制 order -> 找到并复制多个代码文件 -> 拼接成最终 Prompt”这个繁琐的过程，简化为一次点击。

------

## 4. 快速开始 (Quick Start Guide)

### Step 0: 环境部署

- 安装具备文件系统读写能力的 AI 编程助手插件（如 Gemini for VS Code）。
- (可选，推荐) 安装 Oron Helper 插件。

### Step 1: 项目初始化

- 手动或通过 Oron Helper 插件在项目根目录创建 `oron.state.yml`。

### Step 2: 需求规划 (与 Conductor 交互)

1.  打开一个 AI 对话窗口，粘贴 `conductor.prompt.md` 的内容，激活 Conductor 角色。
2.  向 Conductor 下达指令，并**使用 `@workspace` 语法引用 `oron.state.yml` 文件**。
3.  Conductor 会在分析后，直接**提议对 `oron.state.yml` 文件的修改**。
4.  在 IDE 中**接受 (Accept)** AI 提出的变更。文件被自动更新。

### Step 3: 执行任务 (与 Worker 交互)

1.  在 Oron Helper 插件的界面或 `oron.state.yml` 文件中，找到一个可执行的 `PENDING` 任务。
2.  点击任务旁的 **[Copy Worker Prompt]** 按钮 (如果使用 Helper)。插件会将 `order` 和所需代码拼接好，放入剪贴板。
3.  打开**一个新的** AI 对话窗口，粘贴剪贴板的内容。
4.  AI (Worker) 会分析收到的上下文，并提议对相关代码文件的修改。
5.  在 IDE 中**接受**这些代码变更。

### Step 4: 验收与同步

1.  代码应用后，可手动或通过 Helper 插件将 `oron.state.yml` 中对应任务的 `status` 修改为 `COMPLETED` 或 `TESTING`。
2.  在下一轮与 Conductor 的交互中，它将通过读取文件自行发现状态的变更。

------

## 5. 迭代维护指南 (Maintenance)

- **Prompt 维护:** 所有 Prompt 都是独立的 `.md` 文件，用户可自行修改。
- **协议演进:** 对 `oron.state.yml` 结构的任何修改都需要首先在本 Kernel 文档中进行定义，然后更新 Conductor 的 Prompt，使其能够理解和生成新版结构。Helper 插件的解析逻辑也需同步更新。