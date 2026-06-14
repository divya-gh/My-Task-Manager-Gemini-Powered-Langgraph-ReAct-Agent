import streamlit as st
from streamlit_chat import message
from datetime import datetime

from agent.graph import graph
from agent.memory_store import store_memory
from agent.HTML_todo_dashboard import render_html_dashboard
from agent.HTML_patch_viewer import render_patch_html
from langchain_core.messages import HumanMessage, AIMessage
import random

st.set_page_config(page_title="My Task Manager — Gemini LangGraph Agent", layout="wide")

# -------------------------------
# LOGIN SCREEN (Centered & Professional)
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if st.session_state.user_id == "":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 style='text-align: center;'>👋 Welcome to Your AI Task Manager</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:19px;'>Please enter your name to begin.</p>", unsafe_allow_html=True)

        st.markdown(
            "<label style='font-size: 18px; font-weight: 600;'>Your Name:</label>",
            unsafe_allow_html=True
        )

        name = st.text_input(
            "",
            key="login_name",
            placeholder="Type your name here...",
        )

        st.write("")
        st.write("")

        if st.button("Start", use_container_width=True):
            if name.strip():
                st.session_state.user_id = name.strip()
                st.rerun()

    st.stop()

# -------------------------------
# Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.header("📌 Navigation")
    page = st.radio("Go to:", ["Chat", "Task Dashboard", "Memory Store", "Patch Viewer"])

user_id = str(st.session_state.user_id)
config = {"configurable": {"thread_id": user_id, "user_id": user_id}}

                # -------------------------------
        # Initialize session state (once)
        # -------------------------------
if "chat_input_buffer" not in st.session_state:
    st.session_state.chat_input_buffer = ""

if "chat_input" not in st.session_state:
    st.session_state.chat_input = ""

if "send" not in st.session_state:
    st.session_state.send = False

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Wrapper for Streamlit
# -------------------------------
def run_agent_streamlit(user_message):
    result = graph.invoke({"messages": [HumanMessage(content=user_message)]}, config)
    return result["messages"], result.get("patches", None)



# -------------------------------
# Chat Page
# -------------------------------
if page == "Chat":
    if page == "Chat": st.title(f"Hi {user_id}! 👋") 
    st.markdown("""
                    <style>
                        .hero-title {
                            font-size: 38px;
                            font-weight: 700;
                            color: #EAEAEA;
                            margin-bottom: 10px;
                        }

                        .hero-subtitle {
                            font-size: 18px;
                            color: #C0C0C0;
                            margin-bottom: 25px;
                        }

                        .section-header {
                            font-size: 24px;
                            font-weight: 600;
                            color: #D6D6D6;
                            margin-top: 25px;
                            margin-bottom: 15px;
                        }

                        .feature-card {
                            background-color: #2B2B2B;
                            padding: 15px 20px;
                            border-radius: 12px;
                            margin-bottom: 12px;
                            border-left: 5px solid #7A7A7A;
                        }

                        .feature-title {
                            font-size: 18px;
                            font-weight: 600;
                            color: #F0F0F0;
                        }

                        .feature-text {
                            font-size: 15px;
                            color: #D0D0D0;
                        }

                        .nav-box {
                            background-color: #333333;
                            padding: 15px;
                            border-radius: 12px;
                            margin-top: 20px;
                            color: #E0E0E0;
                        }

                        .ready-box {
                            background-color: #3A3A3A;
                            padding: 18px;
                            border-radius: 12px;
                            margin-top: 25px;
                            text-align: center;
                            font-size: 18px;
                            font-weight: 600;
                            color: #F0F0F0;
                        }
                        </style>

                    <div class="hero-title">
                    🧠 Your Personal AI Task Manager Assistant
                    </div>

                    <div class="hero-subtitle">
                    More than a simple to-do list. Your AI-powered productivity partner that learns how you work, adapts to your preferences, and helps you stay organized and focused.
                    </div>

                    <div class="section-header">
                    🚀 What I Can Do
                    </div>

                    <div class="feature-card">
                    <div class="feature-title">✅ Manage Your Tasks</div>
                    <div class="feature-text">
                    Create, update, organize, prioritize, and track tasks while maintaining a personalized to-do list.
                    </div>
                    </div>

                    <div class="feature-card">
                    <div class="feature-title">✅ Provide Intelligent Guidance</div>
                    <div class="feature-text">
                    Analyze your tasks, suggest next actions, identify missing steps, and help you plan effectively.
                    </div>
                    </div>

                    <div class="feature-card">
                    <div class="feature-title">✅ Learn Your Preferences</div>
                    <div class="feature-text">
                    Understand how you prefer to organize and manage work by learning recurring habits and planning styles.
                    </div>
                    </div>

                    <div class="feature-card">
                    <div class="feature-title">✅ Build Your Personal Profile</div>
                    <div class="feature-text">
                    Learn about your interests, goals, and work patterns to provide increasingly personalized recommendations.
                    </div>
                    </div>

                    <div class="feature-card">
                    <div class="feature-title">✅ Reason & Plan Transparently</div>
                    <div class="feature-text">
                    Track how decisions are made, understand the reasoning behind recommendations, and see how your AI assistant works.
                    </div>
                    </div>

                    <div class="nav-box">
                    <b>Explore the Navigation Panel</b><br><br>

                    📋 <b>Task Dashboard</b> — View and manage your tasks<br>
                    🧠 <b>Memory Store</b> — Review learned preferences and profile information<br>
                    🔍 <b>Patch Viewer</b> — See how the AI reasons and makes decisions
                    </div>

                    <div class="ready-box">
                    💬 Ready to get started?<br><br>
                    Ask me about your tasks, goals, projects, travel plans, learning objectives, or anything you'd like help organizing.
                    </div>
                    """, unsafe_allow_html=True)                                


    for i, (role, msg) in enumerate(st.session_state.history):
        message(msg, is_user=(role == "user"), key=f"msg_{i}")

    examples = [
                    " EX: Plan my trip to London this Saturday. I love coffee. Suggest places to visit and remind me when I arrive.",
                    "Remind me to renew my passport next before July31st.",
                    "Help me create a study plan for Ethics in AI.",
                    "Track my job applications and suggest next steps.",
                    "I need to book an appointment Dental cleaning tomorrow at 2PM."
                    "Organize my tasks by priority and deadline."
                ]

    user_message = st.chat_input(
                    placeholder=random.choice(examples)
                )

    if user_message:

        st.session_state.history.append(("user", user_message))

        with st.spinner("Thinking..."):

            response, patches = run_agent_streamlit(user_message)

            final_msg = ""

            ai_messages = [
                m for m in response
                if isinstance(m, AIMessage)
            ]

            if ai_messages:

                last_ai = ai_messages[-1]
                content = last_ai.content

                if (
                    isinstance(content, list)
                    and len(content) > 0
                    and isinstance(content[0], dict)
                ):
                    text = content[0].get("text", "")

                    if text.startswith("AI_response:"):
                        final_msg = text.replace(
                            "AI_response:",
                            ""
                        ).strip()

                elif isinstance(content, str):

                    if content.startswith("AI_response:"):
                        final_msg = content.replace(
                            "AI_response:",
                            ""
                        ).strip()
                    else:
                        final_msg = content

        st.session_state.history.append(("ai", final_msg))

        if patches:
            st.session_state.patches = patches

        st.rerun()


# -------------------------------
# Task Dashboard Page
# -------------------------------
elif page == "Task Dashboard":
    st.subheader("📋 Task Dashboard")
    html = render_html_dashboard(user_id, store_memory)
    st.components.v1.html(html, height=600, scrolling=True)

# -------------------------------
# Memory Store Page
# -------------------------------
elif page == "Memory Store":
    st.subheader("🧠 Long‑Term Memory Store")

    namespaces = [
        ("UserProfile", user_id),
        ("ToDo", user_id),
        ("Instructions", user_id)
    ]

    for ns in namespaces:
        st.markdown(f"### 📌 Namespace: `{ns[0]}` — User: `{ns[1]}`")
        items = store_memory.search(ns)

        if not items:
            st.info("No memory found.")
            continue

        for m in items:
            st.json(m.value)

# -------------------------------
# Patch Viewer Page
# -------------------------------
elif page == "Patch Viewer":
    st.subheader("🔍 Patch Viewer (Tool Call Visibility)")
    if "patches" in st.session_state:
        html = render_patch_html(st.session_state.patches)
        st.components.v1.html(html, height=600, scrolling=True)
    else:
        st.info("No patches yet. Chat with the agent first.")
