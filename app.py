import streamlit as st
import json
import os
from matcher import FAQMatcher
from faq_data import FAQS

CUSTOM_FAQ_FILE = "custom_faqs.json"

# ---------- Page setup ----------
st.set_page_config(page_title="Querio Store — Help Chat", page_icon="💬", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
    .header-banner {
        background: linear-gradient(135deg, #4B3FF2 0%, #7B6EF6 100%);
        padding: 24px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
    }
    .header-title {
        color: white;
        font-size: 26px;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        color: #E5E1FF;
        font-size: 14px;
        margin-top: 4px;
    }
    section[data-testid="stSidebar"] {
        background-color: #F7F7FB;
        border-right: 1px solid #E5E7EB;
    }
    section[data-testid="stSidebar"] button {
        border-radius: 10px !important;
        border: 1px solid #E0DEFB !important;
        text-align: left !important;
        transition: all 0.15s ease;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #EEF0FF !important;
        border-color: #4B3FF2 !important;
        color: #4B3FF2 !important;
    }
    .bubble-row {
        display: flex;
        margin-bottom: 4px;
    }
    .bubble-user {
        justify-content: flex-end;
    }
    .bubble-bot {
        justify-content: flex-start;
    }
    .bubble-content-user {
        background-color: #4B3FF2;
        color: white;
        padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 65%;
        font-size: 15px;
        line-height: 1.4;
    }
    .bubble-content-bot {
        background-color: #FFFFFF;
        border: 1px solid #E9E9EF;
        padding: 10px 16px;
        border-radius: 4px 18px 18px 18px;
        max-width: 65%;
        font-size: 15px;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .bot-avatar {
        font-size: 20px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Custom FAQ storage helpers ----------
def load_custom_faqs():
    if os.path.exists(CUSTOM_FAQ_FILE):
        with open(CUSTOM_FAQ_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_custom_faqs(custom_faqs):
    with open(CUSTOM_FAQ_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_faqs, f, indent=2, ensure_ascii=False)

# ---------- Session state setup ----------
if "custom_faqs" not in st.session_state:
    st.session_state.custom_faqs = load_custom_faqs()

if "matcher" not in st.session_state:
    all_faqs = FAQS + st.session_state.custom_faqs
    st.session_state.matcher = FAQMatcher(all_faqs)

matcher = st.session_state.matcher

FALLBACK_MESSAGE = (
    "I'm sorry, I don't have an answer for that. Try rephrasing your question, "
    "or ask me about returns, shipping, delivery, tracking, payments, cancellations, "
    "account/login, or sizing."
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 📋 Frequently Asked Questions")
    st.caption("Tap a question to ask it directly.")

    all_faqs_for_display = FAQS + st.session_state.custom_faqs
    for faq in all_faqs_for_display:
        primary_question = faq["questions"][0]
        if st.button(primary_question, key=f"faq_{primary_question}", use_container_width=True):
            st.session_state.setdefault("messages", [])
            st.session_state.messages.append({"role": "user", "content": primary_question})
            match, score = matcher.get_best_match(primary_question)
            response = match["answer"] if match else FALLBACK_MESSAGE
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    st.divider()
    with st.expander("➕ Add a New FAQ"):
        with st.form("add_faq_form", clear_on_submit=True):
            new_question = st.text_input("Main question")
            new_variations = st.text_area(
                "Other ways someone might ask this (comma separated, optional)"
            )
            new_answer = st.text_area("Answer")
            submitted = st.form_submit_button("Add FAQ")

            if submitted:
                if not new_question.strip() or not new_answer.strip():
                    st.error("Please fill in at least the question and the answer.")
                else:
                    variations = [v.strip() for v in new_variations.split(",") if v.strip()]
                    new_faq = {
                        "questions": [new_question.strip()] + variations,
                        "answer": new_answer.strip()
                    }
                    st.session_state.custom_faqs.append(new_faq)
                    save_custom_faqs(st.session_state.custom_faqs)
                    matcher.add_faq(new_faq)
                    st.success("FAQ added! It's now live in the chat.")

# ---------- Header ----------
st.markdown("""
<div class="header-banner">
    <p class="header-title">💬 Querio Store — Help Chat</p>
    <p class="header-subtitle">Ask me anything about your order, shipping, returns, or account.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! 👋 I'm the Querio Store assistant. Ask me about returns, shipping, payments, or your order."}
    ]
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="bubble-row bubble-user">
            <div class="bubble-content-user">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bubble-row bubble-bot">
            <span class="bot-avatar">🤖</span>
            <div class="bubble-content-bot">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Feedback reactions, only under real bot answers (skip the opening greeting)
        if i > 0:
            if st.session_state.feedback.get(i) is None:
                col1, col2, col3, _ = st.columns([1, 1, 1, 7])
                with col1:
                    if st.button("😃", key=f"good_{i}"):
                        st.session_state.feedback[i] = "good"
                        st.rerun()
                with col2:
                    if st.button("😐", key=f"okay_{i}"):
                        st.session_state.feedback[i] = "okay"
                        st.rerun()
                with col3:
                    if st.button("😞", key=f"bad_{i}"):
                        st.session_state.feedback[i] = "bad"
                        st.rerun()
            else:
                labels = {
                    "good": "Glad that helped! 😃",
                    "okay": "Thanks for the feedback. 😐",
                    "bad": "Sorry about that — I'll keep improving. 😞"
                }
                st.caption(labels[st.session_state.feedback[i]])

# ---------- Chat input ----------
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    match, score = matcher.get_best_match(user_input)
    response = match["answer"] if match else FALLBACK_MESSAGE
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()