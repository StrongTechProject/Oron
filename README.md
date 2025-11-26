<p align="right">
  English | <a href="./README.zh.md">中文</a>
</p>



# Oron Framework



**The Dual-Entity Software Engineering Framework for Infinite-Context Development.**

> **Design Philosophy:** "Binary Divide and Conquer + Atomic Dispatch + Tool Bridging."

Oron is a strictly defined architecture designed to solve the physical bottlenecks of Large Language Models (LLMs) in complex software engineering: **Context Decay**, **Context Air-Gap**, **IO Fatigue**, and **Output Overload**. It separates the "Brain" (Conductor) from the "Hands" (Worker), bridged by a local Python adapter.

------



## 1. Project Positioning



Oron is not just a prompt; it is a **Layered Development Framework** based on the v1.0.1 Architecture Definition Document (ADD). It addresses the fundamental limitation of single-agent coding: as conversations grow, intelligence drops.

Oron implements a **State-Machine-Driven** approach where:

1. **The Conductor (Brain):** Maintains the project state, dependency graph, and plans logic. It *never* writes implementation code.
2. **The Worker (Hands):** Executes specific, atomic coding tasks in a stateless environment.
3. **The Adapter (Middleware):** Automates the friction of context gathering and prompt injection.

------



## 2. Pain Points & Solution Comparison



Standard LLM interactions degrade rapidly during complex projects. Oron introduces **WGC (Worker Granularity Control)** to maintain high-quality output indefinitely.



### The Problems Oron Solves



| **Pain Point**           | **Standard LLM Generation**                                  | **Oron Architecture**                                        |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Context Window Decay** | As chat history grows, the model forgets early requirements and hallucinates. | **Solved:** Worker is stateless/fresh every turn. Only relevant context is injected. |
| **Output Overload**      | Generating 300+ lines at once results in "lazy coding" (e.g., `# ... rest of code`). | **Solved via WGC:** Enforces "Atomic Dispatch." Tasks are split into micro-steps (<150 lines). |
| **Context Air-Gap**      | The Architect needs to see every line of code, wasting token budget. | **Solved:** Conductor only stores "Interface Signatures"; Worker sees the Implementation. |
| **IO Fatigue**           | Manually copying file contents and pasting code blocks is exhausting. | **Solved:** `oron.py` automates context reading and clipboard injection. |



### Performance Projection (Estimated)



*Comparing a standard complex feature implementation vs. Oron v1.0.1 flow.*

| **Metric**           | **Standard Chat**          | **Oron Framework**  | **Impact**               |
| -------------------- | -------------------------- | ------------------- | ------------------------ |
| **Context Clarity**  | Decays after 4k tokens     | **Constant (100%)** | 🟢 No hallucination drift |
| **Code Validity**    | ~60% (needs manual fixing) | **~95%**            | 🟢 Due to Atomic Focus    |
| **Token Efficiency** | Low (Full file re-reads)   | **High**            | 🟢 Specific slicing       |
| **Project Lifespan** | 1-2 features before reset  | **Infinite**        | 🟢 Modular State Machine  |

------



## 3. System Architecture



The system follows a strict 3-Layer Topology:

```
graph TD
    User((User))
    
    subgraph Layer_2_Core ["Layer 2: The Core (Conductor)"]
        State[State Machine (YAML)]
        Plan[Planning & Logic]
    end
    
    subgraph Layer_3_Adapter ["Layer 3: The Adapter (Local)"]
        OronPy["oron.py Script"]
        IO[File System I/O]
    end
    
    subgraph Worker_Scope ["Stateless Worker"]
        Exec[Code Generation]
    end

    User -->|Prompts| Plan
    Plan -->|Generates CLI Cmd| User
    User -->|Runs Command| OronPy
    OronPy -->|Reads Context| IO
    OronPy -->|Injects Context + Prompt| Exec
    Exec -->|Returns Code| User
    User -->|Verifies & Updates| State
```

1. **Layer 1 (Kernel):** The Constitution (Rules & Constraints).
2. **Layer 2 (Core):** The System Prompt (Conductor Intelligence).
3. **Layer 3 (Adapter):** The `oron.py` script (I/O & WGC Enforcement).

------



## 4. Installation & Usage



Oron requires a lightweight local adapter to handle file operations and clipboard management.



### Requirements



- Python 3.x
- `pyperclip` (for clipboard automation)



### Installation



1. Clone this repository or create the script manually.

2. Install the dependency:

   Bash

   ```
   pip install pyperclip
   ```

3. Ensure `oron.py` is in your project root.



### CLI Usage



The Conductor will generate these commands for you, but understanding the syntax is helpful.

**Syntax:**

Bash

```
python oron.py inject --files "<file_list>" --task "<instruction>"
```

**Arguments:**

- `--files`: Comma-separated list of file paths (e.g., `app/main.py,app/utils.py`).
  - *Note:* If a file doesn't exist, Oron v1.0.1 activates **Creation Mode** (Soft Fail) instead of erroring out.
- `--task`: A concise instruction string for the Worker.

------



## 5. Quick Start (1 Minute Guide)



Follow the **Step 0-2** flow defined in the ADD.



### Step 0: Environment Prep



Download `oron.py` to your project folder.

Bash

```
pip install pyperclip
```



### Step 1: Activate the Conductor (The Brain)



1. Open an LLM session (Claude 3.5 Sonnet / GPT-4o recommended).
2. Copy the **Core Spell v1.0.1** (System Prompt) from `prompts/core_spell.md`.
3. Paste it into the chat.
4. State your project goal: *"I want to build a Snake game in Python."*



### Step 2: The Loop (Development Cycle)



1. **Receive Instruction:** The Conductor will output a command like:

   Bash

   ```
   python oron.py inject --files "game.py" --task "Initialize Pygame window and game loop."
   ```

2. **Execute Adapter:** Paste that command into your terminal.

   - *Result:* Context and instructions are automatically copied to your clipboard.

3. **Dispatch to Worker:** Open a **new/separate** LLM window (The Worker) and press `Ctrl+V`.

4. **Verify & Sync:** Copy the code generated by the Worker into your local file.

5. **Report:** Tell the Conductor: *"VERIFIED"* or *"FAILED: <error message>"*.

------



## 6. Core Features & Key Technologies





### ⚡ WGC (Worker Granularity Control)



Introduced in v1.0.1, this protocol prevents "Context Overflow." The Conductor strictly adheres to the **Rule of Three**:

- Max **3 files** touched per turn.
- Max **1 functional logic** per turn.
- Max **150 lines** of code output per turn.



### 🧠 Smart Context Injection



The `oron.py` adapter is context-aware:

- **Reading Mode:** Reads files with line numbers for precise editing.
- **Creation Mode:** If a file is missing, it suppresses errors and prompts the Worker to create it from scratch.



### 🛡️ Interface Signature ACL



The Conductor maintains a "Memory Bank" in its YAML state. It only remembers **Function Signatures** (e.g., `def connect_db(url) -> bool`), discarding implementation details to save memory and keep the architectural view clean.



### 🔄 Fission Check



Before issuing a command, the Conductor performs a "Fission Check." If a task is too complex, it splits it into `Task 1.1`, `Task 1.2`, ensuring the Worker never fails due to complexity overload.

------

*Copyright © 2025 Oron Project. Defined by ADD v1.0.1.*