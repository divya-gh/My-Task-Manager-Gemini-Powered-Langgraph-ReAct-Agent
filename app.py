import streamlit as st
from streamlit_chat import message
from datetime import datetime

from agent.graph import graph
from agent.memory_store import store_memory
from agent.HTML_todo_dashboard import render_html_dashboard
from agent.HTML_patch_viewer import render_patch_html
from langchain_core.messages import HumanMessage, AIMessage

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
    st.subheader("I'm your AI Task Manager.") 
    st.markdown(""" I can help you: - Log tasks and update your to‑do list 
                - Remember your preferences and profile 
                - Learn about how you like your tasks to be managed 
                - Show you exactly how I think using Patch Viewer """) 
    st.markdown( "<p style='font-size:20px; font-weight:700; text-align:center; color:#2A4D69;'>" 
                "Go ahead and start chatting with me in the <b>Chat</b> tab." "</p>", 
                unsafe_allow_html=True ) 
    st.markdown(""" And don’t forget to check your **Task Dashboard** & **Memory Store** to see what I’ve learned about you! """) 
    st.markdown( "<h2 style='text-align:center; color:#808080; font-weight:700;'>💬 Chat with Your AI Agent</h2>", unsafe_allow_html=True ) 
    col1, col2, col3 = st.columns([1, 3, 1]) 
    
    with col2: 
        st.markdown( "<p style='font-size:18px; font-weight:600; text-align:left; margin-bottom:6px;'>How can I help you today?</p>", 
                    unsafe_allow_html=True )

    st.title(f"Hi {user_id}! 👋")

    for i, (role, msg) in enumerate(st.session_state.history):
        message(msg, is_user=(role == "user"), key=f"msg_{i}")

    user_message = st.chat_input("Type a message")

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
