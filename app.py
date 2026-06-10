import streamlit as st
from pymongo import MongoClient
import bcrypt
import pdfplumber
import requests
import uuid
from datetime import datetime

client = MongoClient("mongodb://mongodb:27017/")
db = client["ai_app"]
users = db["users"]
docs = db["documents"]
chats = db["chats"]

for k, v in {"user": "", "active_chat": None, "history": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.set_page_config(page_title="TrueLineQA", layout="centered")

st.markdown("""
<style>
#MainMenu, footer { visibility: hidden; }
.stApp { background-color: #f5f5f3; font-size: 16px; }

/* ── Typography ── */
h1 { font-size: 32px !important; font-weight: 700 !important; color: #111 !important; margin-bottom: 4px !important; letter-spacing: -0.5px; }
h2 { font-size: 24px !important; font-weight: 600 !important; color: #111 !important; margin-bottom: 2px !important; }
h3 { font-size: 20px !important; font-weight: 600 !important; color: #222 !important; }
p  { font-size: 16px; line-height: 1.6; color: #333; }

/* ── Auth page ── */
.auth-title {
    font-size: 32px;
    font-weight: 700;
    color: #111;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}
.auth-sub {
    font-size: 15px;
    color: #888;
    margin-bottom: 28px;
    line-height: 1.5;
}

/* ── Input fields ── */
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input {
    font-size: 15px !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    border: 1.5px solid #ddd !important;
    background: #fff !important;
    color: #111 !important;
    transition: border-color 0.2s !important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="base-input"] input:focus {
    border-color: #111 !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06) !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #aaa !important;
    font-size: 14px !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #fff !important;
    color: #111 !important;
    border: 1.5px solid #ccc !important;
    border-radius: 8px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    width: 100%;
    transition: background 0.2s, transform 0.1s;
}
.stButton > button:hover  { background-color: #f0f0ec !important; border-color: #aaa !important; }
.stButton > button:active { transform: scale(0.98); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #eaeae7;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    color: #888;
    font-size: 14px;
    font-weight: 500;
    padding: 6px 18px;
}
.stTabs [aria-selected="true"] {
    background: #fff !important;
    color: #111 !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #fafaf8 !important;
    border-right: 1px solid #e5e5e0 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background-color: #f0f0ec !important;
    color: #333 !important;
    border: 1px solid #e0e0db !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #e5e5e0 !important;
    color: #111 !important;
}

/* ── Sidebar brand ── */
.sidebar-brand {
    font-size: 20px;
    font-weight: 700;
    color: #111;
    letter-spacing: -0.3px;
}
.sidebar-user {
    font-size: 12px;
    color: #999;
    margin-top: 2px;
    margin-bottom: 0;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    border: 1px solid #e8e8e4 !important;
    background: #fff !important;
}

/* ── Chat input bar ── */
[data-testid="stChatInput"] textarea {
    font-size: 15px !important;
    border: 1.5px solid #ddd !important;
    border-radius: 10px !important;
    background: #fff !important;
    padding: 12px 16px !important;
    line-height: 1.5 !important;
    color: #111 !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #111 !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.06) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #bbb !important;
    font-size: 14px !important;
}

/* ── File uploader (no drag slider) ── */
[data-testid="stFileUploader"] {
    background: #fff;
    border: 1.5px dashed #ccc;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
}

/* ── Active chat name ── */
.chat-doc-name {
    font-size: 13px;
    color: #888;
    font-weight: 400;
    margin-top: -8px;
    margin-bottom: 12px;
}

/* ── Alert ── */
.stAlert { border-radius: 8px; font-size: 14px; }

/* ── Divider ── */
hr { border-color: #e5e5e0; margin: 14px 0; }

/* ── Section label in sidebar ── */
.sidebar-section {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    color: #aaa;
    text-transform: uppercase;
    margin: 12px 0 6px 0;
}
</style>
""", unsafe_allow_html=True)


def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

def check_password(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed)

def get_user_chats():
    return list(chats.find({"user": st.session_state.user}).sort("created_at", -1))

def load_chat(chat_id):
    chat = chats.find_one({"chat_id": chat_id})
    if chat:
        st.session_state.active_chat = chat_id
        st.session_state.history = chat.get("history", [])

def ask_groq(context, question):
    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": "YOUR_API_KEY",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Answer only based on the provided document context. Be helpful and concise."},
                    {"role": "user", "content": f"Document context:\n{context}\n\nQuestion: {question}"}
                ]
            },
            timeout=30
        )
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Something went wrong: {str(e)}"


# ── Auth page ─────────────────────────────────────────────────────────────────
def auth_page():
    st.markdown('<p class="auth-title">TrueLineQA</p>', unsafe_allow_html=True)
    st.markdown('<p class="auth-sub">Upload a document. Ask questions. Get precise answers.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username", placeholder="Enter your username", key="li_u")
        p = st.text_input("Password", type="password", placeholder="Enter your password", key="li_p")
        if st.button("Login", key="li_btn"):
            user = users.find_one({"username": u})
            if user and check_password(p, user["password"]):
                st.session_state.user = u
                st.session_state.history = []
                st.session_state.active_chat = None
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        ru = st.text_input("Choose a username", placeholder="Pick a username", key="reg_u")
        rp = st.text_input("Choose a password", type="password", placeholder="Pick a strong password", key="reg_p")
        if st.button("Create Account", key="reg_btn"):
            if not ru or not rp:
                st.warning("Please fill in both fields")
            elif users.find_one({"username": ru}):
                st.error("Username already taken")
            else:
                users.insert_one({"username": ru, "password": hash_password(rp)})
                st.success("Account created! Go to Login.")


# ── Chat page ─────────────────────────────────────────────────────────────────
def chat_page():

    with st.sidebar:
        st.markdown(f'<p class="sidebar-brand">TrueLineQA</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sidebar-user">Signed in as {st.session_state.user}</p>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<p class="sidebar-section">New Chat</p>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
        if uploaded_file is not None:
            if st.button("Start chat with this PDF"):
                text = ""
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                if not text.strip():
                    st.error("Could not read text from this PDF.")
                else:
                    chat_id = str(uuid.uuid4())
                    chats.insert_one({
                        "chat_id": chat_id,
                        "user": st.session_state.user,
                        "filename": uploaded_file.name,
                        "content": text,
                        "history": [],
                        "created_at": datetime.utcnow()
                    })
                    st.session_state.active_chat = chat_id
                    st.session_state.history = []
                    st.rerun()

        st.divider()

        # ── Past chats with delete ────────────────────────────────────────────
        user_chats = get_user_chats()
        if user_chats:
            st.markdown('<p class="sidebar-section">Your Chats</p>', unsafe_allow_html=True)
            for c in user_chats:
                is_active = c["chat_id"] == st.session_state.active_chat
                name = c["filename"]
                name_display = (name[:22] + "...") if len(name) > 25 else name

                col1, col2 = st.columns([5, 1])
                with col1:
                    label = f"» {name_display}" if is_active else name_display
                    if st.button(label, key=f"open_{c['chat_id']}"):
                        load_chat(c["chat_id"])
                        st.rerun()
                with col2:
                    if st.button("x", key=f"del_{c['chat_id']}"):
                        chats.delete_one({"chat_id": c["chat_id"]})
                        if st.session_state.active_chat == c["chat_id"]:
                            st.session_state.active_chat = None
                            st.session_state.history = []
                        st.rerun()
        else:
            st.caption("No chats yet.")

        st.divider()
        if st.button("Logout"):
            st.session_state.user = ""
            st.session_state.history = []
            st.session_state.active_chat = None
            st.rerun()

    # ── Main area ─────────────────────────────────────────────────────────────
    if not st.session_state.active_chat:
        st.markdown("## TrueLineQA")
        st.markdown('<p style="color:#999;font-size:15px;margin-top:-6px;">Upload a PDF from the sidebar to start a new chat.</p>', unsafe_allow_html=True)
        return

    active = chats.find_one({"chat_id": st.session_state.active_chat})
    if not active:
        st.session_state.active_chat = None
        st.session_state.history = []
        st.rerun()

    st.markdown("## TrueLineQA")
    st.markdown(f'<p class="chat-doc-name">Chatting with: {active["filename"]}</p>', unsafe_allow_html=True)
    st.divider()

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(f'<span style="font-size:15px;line-height:1.6;">{msg["content"]}</span>', unsafe_allow_html=True)

    q = st.chat_input("Ask something about your document...")

    if q:
        st.session_state.history.append({"role": "user", "content": q})
        context = active["content"][:3000]
        ans = ask_groq(context, q)
        st.session_state.history.append({"role": "assistant", "content": ans})
        chats.update_one(
            {"chat_id": st.session_state.active_chat},
            {"$set": {"history": st.session_state.history}}
        )
        st.rerun()


if st.session_state.user:
    chat_page()
else:
    auth_page()