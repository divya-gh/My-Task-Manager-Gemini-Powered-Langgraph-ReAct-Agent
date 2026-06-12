# 📌 My Task Manager — Gemini‑Powered LangGraph ReAct Agent
**A powerful, intelligent task‑management AI assistant that can reason, use tools, update long‑term memory, manage tasks, and even generate customized To‑Do cards — all inside a ReAct‑style workflow.**

`Agent is built using Gemini, LangGraph, TrustCall, and a custom SPY listener for full visibility into tool calls and JSON Patch updates.`

### 🧠 How It Works
**Below is a clean workflow diagram**

              ┌──────────────────────────┐
                │        User Input         │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │     Gemini LLM (ReAct)    │
                │  Thought → Tool → Answer  │
                └─────────────┬────────────┘
                              │
                ┌─────────────┼──────────────┐
                ▼             ▼               ▼
      ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐
      │ UserProfile     │  │ ToDoItem       │  │ InstructionMemory  │
      │ TrustCall Tool  │  │ TrustCall Tool │  │ TrustCall Tool     │
      └────────────────┘  └────────────────┘  └────────────────────┘
                │             │               │
                └─────────────┼──────────────┘
                              ▼
                ┌──────────────────────────┐
                │     Memory Store          │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │     SPY Listener          │
                │  (Tool Call Visibility)   │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │   HTML Patch Viewer       │
                └──────────────────────────┘

## 🚀 What This Agent Can Do

### 📝 1. Manage a Smart To‑Do List
- Add new tasks
- Update existing tasks
- Mark tasks as completed
- Understand natural language like: “Remind me to buy milk tomorrow morning.”
- Moniter date and time
- provide solution to complete the task
- capable of classifying `semantic memory` {profile,collections} and procedural memory.
- Store each task as its own Long term memory document


### 🧠 2. Maintain a User Profile
**Automatically learns and updates:**
- Name
- age
- Location
- Job
- relations
- Preferences & interests
- Habits
- Routines

Example:
“I prefer almond milk.” → stored instantly.

### 📘 3. Learn and Improve Its Own Behavior
**The agent maintains an Instruction Memory, allowing it to:**
- Learn new rules
- Adjust its behavior
- Improve task‑handling logic
Example:
“Always ask for a due date when I add tasks.”

### 🔧 4. Structured Memory Updates with TrustCall
**TrustCall enables:**
- Schema‑validated extraction
- SON Patch updates
- Insert + update logic
- Automatic self‑correction
- Three schemas power the system:
    - UserProfile
    - ToDoItem
    - InstructionMemory

### 🕵️‍♂️ 5. Full Transparency with SPY Listener
**The custom SPY tool logs:**
- Tool calls
- PatchDoc updates
- Validation corrections
- New memory creation
- Plus a beautiful HTML Patch Viewer to inspect changes visually.

## 🛠️ How It’s Built

###🔹 Gemini LLM
Handles reasoning, tool calling, and final answers.

### 🔹 LangGraph
**Builds the ReAct agent workflow:**
- LLM node
- Tool router
- Memory writer
- Final answer node

###🔹 TrustCall API
**Provides:**
- Structured extraction
- JSON Patch updates
- Insert + update logic
- Validation and self‑correction

###🔹 SPY Listener
**Captures:**
- Tool calls
- PatchDoc updates
 -Validation errors
- New memory creation

### 🔹 HTML Patch Viewer
**Visualizes:**
- Planned edits
- Actual updates
- Document IDs
- Before/after states with color

Image

## 📌 Future Enhancements
- Task prioritization
- Deadlines and reminders
- Calendar integration
- Natural‑language search
- Task categories
- Voice interface
- Deployment to cloud

### Citation: 
This project is an enhancement of the LangGraph project from LangChain Academy, extending it with Gemini‑powered reasoning, HTML card todo list.
