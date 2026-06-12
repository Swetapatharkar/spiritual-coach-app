import streamlit as st
import requests
from datetime import date, datetime

BASE_URL = "https://spiritual-coach-app.onrender.com"

st.set_page_config(
    page_title="Spiritual Coach",
    page_icon="🕉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #e8e0f0 !important;
}

.stApp {
    background-color: #0f0a1e !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #130d28 !important;
    border-right: 0.5px solid rgba(200,168,75,0.18) !important;
}
[data-testid="stSidebar"] * { color: #c8b8e8 !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: #c8a84b !important;
    letter-spacing: 0.04em;
}

/* ── Topbar area ── */
.topbar {
    background: #1a1035;
    border-bottom: 0.5px solid rgba(200,168,75,0.18);
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.topbar-title { font-size: 17px; font-weight: 500; color: #e8e0f0; }
.topbar-date  { font-size: 12px; color: rgba(200,168,75,0.7); margin-top: 2px; }

/* ── Cards ── */
.soul-card {
    background: #1a1035;
    border: 0.5px solid rgba(200,168,75,0.22);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 10px;
}
.soul-card-accent {
    background: #1a1035;
    border-left: 3px solid #c8a84b;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 8px;
}

/* ── Stat cards ── */
.stat-card {
    background: #1a1035;
    border: 0.5px solid rgba(200,168,75,0.22);
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.stat-value { font-size: 26px; font-weight: 500; color: #c8a84b; line-height: 1.1; }
.stat-label { font-size: 11px; color: rgba(200,168,75,0.6); margin-top: 3px; text-transform: uppercase; letter-spacing: 0.07em; }

/* ── Verse banner ── */
.verse-banner {
    background: linear-gradient(135deg, #1a1035 0%, #2d1f6e 100%);
    border: 0.5px solid rgba(200,168,75,0.25);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 16px;
}
.verse-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(200,168,75,0.65); margin-bottom: 6px; font-family: 'Inter', sans-serif; }
.verse-quote { font-size: 14px; color: rgba(255,255,255,0.92); line-height: 1.6; font-style: italic; }
.verse-source { font-size: 12px; color: rgba(200,168,75,0.6); margin-top: 8px; }

/* ── Routine checklist ── */
.routine-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 0.5px solid rgba(200,168,75,0.1);
    font-size: 13px;
    color: #c8b8e8;
}
.routine-item:last-child { border-bottom: none; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 24px 16px;
    color: rgba(200,168,75,0.45);
    font-size: 13px;
    line-height: 1.6;
}

/* ── Streak pill ── */
.streak-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(200,168,75,0.12);
    border: 0.5px solid rgba(200,168,75,0.3);
    border-radius: 20px;
    padding: 5px 12px;
    color: #c8a84b;
    font-size: 12px;
    font-weight: 500;
}

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 0.5px solid rgba(200,168,75,0.15);
    padding-bottom: 8px;
    margin-bottom: 12px;
}
.section-title {
    font-family: 'Cinzel', serif;
    font-size: 14px;
    font-weight: 500;
    color: #c8a84b;
}
.section-badge {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 10px;
    border: 0.5px solid rgba(200,168,75,0.25);
    color: rgba(200,168,75,0.65);
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background: rgba(26,16,53,0.95) !important;
    border: 0.5px solid rgba(200,168,75,0.3) !important;
    border-radius: 8px !important;
    color: #e8e0f0 !important;
    caret-color: #c8a84b !important;
    -webkit-text-fill-color: #e8e0f0 !important;
}

/* Placeholder text */
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(200,168,75,0.35) !important;
    -webkit-text-fill-color: rgba(200,168,75,0.35) !important;
}

/* Focused border glow */
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: rgba(200,168,75,0.6) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(200,168,75,0.1) !important;
}

/* Selectbox dropdown option text */
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #e8e0f0 !important;
    -webkit-text-fill-color: #e8e0f0 !important;
}

.stTextInput label, .stTextArea label, .stSelectbox label,
.stCheckbox label, .stDateInput label, .stRadio label {
    color: rgba(200,168,75,0.8) !important;
    font-size: 12px !important;
    letter-spacing: 0.03em;
}

/* ── Buttons ── */
.stButton > button {
    background: #1a1035 !important;
    color: #c8a84b !important;
    border: 0.5px solid rgba(200,168,75,0.4) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 0.45rem 1.2rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: background 0.15s, transform 0.1s;
}
.stButton > button:hover {
    background: rgba(200,168,75,0.1) !important;
    transform: translateY(-1px);
}
.stButton > button:active { transform: scale(0.98); }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #1a1035 !important;
    border: 0.5px solid rgba(200,168,75,0.22) !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
}
[data-testid="metric-container"] label {
    color: rgba(200,168,75,0.65) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c8a84b !important;
    font-size: 24px !important;
    font-weight: 500;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: rgba(26,16,53,0.8) !important;
    border-radius: 8px !important;
    gap: 2px !important;
    padding: 3px !important;
}
[data-baseweb="tab"] {
    color: rgba(200,168,75,0.55) !important;
    font-size: 13px !important;
    border-radius: 6px !important;
}
[aria-selected="true"] {
    color: #c8a84b !important;
    background: rgba(200,168,75,0.12) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #1a1035 !important;
    border: 0.5px solid rgba(200,168,75,0.18) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: rgba(200,168,75,0.85) !important; }

/* ── Progress bar ── */
.stProgress > div > div { background: rgba(200,168,75,0.15) !important; border-radius: 4px; }
.stProgress > div > div > div { background: #c8a84b !important; border-radius: 4px; }

/* ── Divider ── */
hr { border-color: rgba(200,168,75,0.15) !important; }

/* ── Checkbox ── */
.stCheckbox { color: #c8b8e8 !important; }

/* ── Info / success / error boxes ── */
.stAlert { border-radius: 8px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0f0a1e; }
::-webkit-scrollbar-thumb { background: rgba(200,168,75,0.25); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Constants ────────────────────────────────────────────────────────────────
MOOD_EMOJI = {
    "Peaceful": "☮️", "Grateful": "🙏", "Happy": "😊", "Inspired": "💡",
    "Motivated": "🔥", "Anxious": "😰", "Sad": "😢", "Angry": "😤",
    "Confused": "😕", "Hopeful": "🌅"
}
MOODS = list(MOOD_EMOJI.keys())

DAILY_VERSE = (
    '"You have the right to perform your actions, '
    'but you are not entitled to the fruits of your actions."',
    "Bhagavad Gita 2.47"
)


# ─── Helper: section card wrapper ─────────────────────────────────────────────
def section_card(title: str, badge: str = ""):
    badge_html = f'<span class="section-badge">{badge}</span>' if badge else ""
    st.markdown(
        f'<div class="section-header">'
        f'<span class="section-title">{title}</span>'
        f'{badge_html}</div>',
        unsafe_allow_html=True
    )


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div style="padding: 20px 16px 14px; border-bottom: 0.5px solid rgba(200,168,75,0.15);">
        <div style="font-size: 28px; color: #c8a84b; margin-bottom: 4px;">ॐ</div>
        <div style="font-family:'Cinzel',serif; color: rgba(255,255,255,0.9);
                    font-size: 14px; letter-spacing: 0.05em;">Spiritual Coach</div>
        <div style="font-size: 10px; color: rgba(200,168,75,0.4); letter-spacing: 0.1em;
                    text-transform: uppercase; margin-top: 2px;">Your daily sadhana</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 10px 12px 4px;
                font-size: 9px;
                text-transform: uppercase;
                letter-spacing: 0.1em;
                color: rgba(255,255,255,0.25);">
    Practice
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Dashboard",
            "✨  Affirmations",
            "📖  Journal",
            "🌅  Morning Routine",
            "📿  Sankalp",
            "🙏  Gratitude"
        ],
        label_visibility="collapsed"
    )

    r_streak = requests.get(
        f"{BASE_URL}/journal/stats/streak"
    )

    streak = (
        r_streak.json().get("current_streak", 0)
        if r_streak.status_code == 200
        else 0
    )

    st.markdown(f"""
    <div style="margin-top:20px; padding:14px 14px 16px;
                border-top:0.5px solid rgba(200,168,75,0.1);">
        <span class="streak-pill">🔥 {streak}-day streak</span>
    </div>
    <div style="padding:0 14px 18px;
                font-size:11px;
                color:rgba(200,168,75,0.35);
                font-family:'Cinzel',serif;">
        ॐ नमः शिवाय
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
  
if page == "🏠  Dashboard":

    # Topbar
    today_str = date.today().strftime("%A, %d %B %Y")

    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">Good morning 🙏</div>
            <div class="topbar-date">{today_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Daily verse banner
    st.markdown(f"""
    <div class="verse-banner">
        <div class="verse-label">📿 Verse of the day</div>
        <div class="verse-quote">{DAILY_VERSE[0]}</div>
        <div class="verse-source">— {DAILY_VERSE[1]}</div>
    </div>
    """, unsafe_allow_html=True)

    # rest of dashboard code...

    # Stat cards
    r1 = requests.get(f"{BASE_URL}/sankalp")
    r2 = requests.get(f"{BASE_URL}/gratitude")
    r3 = requests.get(f"{BASE_URL}/journal/stats/streak")
    r4 = requests.get(f"{BASE_URL}/affirmations")

    total_s  = len(r1.json()) if r1.status_code == 200 else 0
    total_g  = len(r2.json()) if r2.status_code == 200 else 0
    streak_v = r3.json().get("current_streak", 0) if r3.status_code == 200 else 0
    total_a  = len(r4.json()) if r4.status_code == 200 else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, value, label in [
        (c1, "🔥", streak_v, "Day streak"),
        (c2, "📖", 0, "Journal entries"),   # replace 0 with real count if endpoint exists
        (c3, "✨", total_a, "Affirmations"),
        (c4, "🙏", total_g, "Gratitudes"),
    ]:
        col.markdown(f"""
        <div class="stat-card">
            <div style="font-size:20px;">{icon}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two-col: Sankalp + Morning Routine
    col_a, col_b = st.columns(2)

    with col_a:
        section_card("📿 Today's Sankalp")
        rs = requests.get(f"{BASE_URL}/sankalp/{date.today()}")
        if rs.status_code == 200:
            s = rs.json()
            st.markdown(
                f'<div class="soul-card">'
                f'<p style="font-style:italic; color:#fff; font-size:14px; line-height:1.6;">'
                f'"{s["sankalp"]}"</p></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
            <div class="soul-card">
                <div class="empty-state">
                    📿<br>No Sankalp set for today.<br>
                    <small>Head to Sankalp to set your intention.</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        section_card("🌅 Morning Routine")
        rm = requests.get(f"{BASE_URL}/morning-routine/{date.today()}")
        if rm.status_code == 200:
            m = rm.json()
            items = {
                "🚶 Walk": m["walk"], "🧘 Yoga": m["yoga"],
                "☀️ Surya Arghya": m["surya_arghya"],
                "💧 Shiva Jal": m["shiva_jal"],
                "📿 Vishnu Sahasranamam": m["vishnu_sahasranamam"]
            }
            done = sum(v for v in items.values())
            st.markdown('<div class="soul-card">', unsafe_allow_html=True)
            st.progress(done / 5, text=f"{done}/5 completed")
            for k, v in items.items():
                icon = "✅" if v else "⭕"
                color = "#e8e0f0" if v else "rgba(200,168,75,0.4)"
                strike = "text-decoration:line-through;" if v else ""
                st.markdown(
                    f'<div class="routine-item">'
                    f'<span>{icon}</span>'
                    f'<span style="color:{color};{strike}">{k}</span></div>',
                    unsafe_allow_html=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="soul-card">
                <div class="empty-state">
                    🌅<br>No routine logged today.<br>
                    <small>Head to Morning Routine to log yours.</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Affirmation strip (full width)
    r_aff = requests.get(f"{BASE_URL}/affirmations")
    if r_aff.status_code == 200 and r_aff.json():
        aff = r_aff.json()[-1]  # latest
        st.markdown(f"""
        <div class="soul-card" style="display:flex; align-items:center; gap:14px;">
            <span style="font-size:20px; flex-shrink:0;">✨</span>
            <span style="font-size:13px; font-style:italic; color:#e8e0f0; line-height:1.5; flex:1;">
                "{aff['text']}"
            </span>
            <span style="font-size:10px; color:rgba(200,168,75,0.4);">Today's affirmation</span>
        </div>
        """, unsafe_allow_html=True)

    # Latest gratitude
    section_card("🙏 Latest Gratitude")
    rg = requests.get(f"{BASE_URL}/gratitude")
    if rg.status_code == 200:
        entries = rg.json()[:3]
        if entries:
            cols = st.columns(len(entries))
            for i, item in enumerate(entries):
                with cols[i]:
                    dt = datetime.fromisoformat(item["created_at"]).strftime("%d %b")
                    st.markdown(
                        f'<div class="soul-card-accent">'
                        f'<p style="font-style:italic; color:#e8e0f0; font-size:13px; '
                        f'line-height:1.5; margin:0;">🙏 {item["gratitude"]}</p>'
                        f'<p style="font-size:10px; color:rgba(200,168,75,0.5); margin:4px 0 0;">{dt}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown("""
            <div class="soul-card">
                <div class="empty-state">🙏<br>No gratitude entries yet today.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# AFFIRMATIONS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✨  Affirmations":
    st.markdown("# ✨ Affirmations")
    st.markdown('<p style="color:rgba(200,168,75,0.65); font-size:13px;">Plant seeds of positivity in your mind.</p>', unsafe_allow_html=True)

    with st.form("aff_form", clear_on_submit=True):
        aff_text = st.text_input("New affirmation", placeholder="I am peaceful, strong, and divine...")
        if st.form_submit_button("💫 Save affirmation"):
            if not aff_text.strip():
                st.error("Please enter an affirmation.")
            else:
                r = requests.post(f"{BASE_URL}/affirmations", json={"text": aff_text})
                st.success("Affirmation saved! 🌺") if r.status_code == 200 else st.error(r.text)

    section_card("Your affirmations")
    r = requests.get(f"{BASE_URL}/affirmations")
    if r.status_code == 200:
        affs = r.json()
        if affs:
            cols = st.columns(2)
            for i, a in enumerate(reversed(affs)):
                with cols[i % 2]:
                    st.markdown(
                        f'<div class="soul-card-accent">'
                        f'<p style="font-style:italic; color:#e8e0f0; font-size:14px; '
                        f'line-height:1.6; margin:0;">✨ {a["text"]}</p>'
                        f'<p style="font-size:10px; color:rgba(200,168,75,0.4); margin:4px 0 0;">#{a["id"]}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown('<div class="empty-state">No affirmations yet. Add your first one above!</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# JOURNAL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📖  Journal":
    st.markdown("# 📖 Journal")

    tab1, tab2, tab3 = st.tabs(["✍️  New entry", "📚  View & delete", "📊  Stats"])

    with tab1:
        with st.form("journal_form", clear_on_submit=True):
            j_title   = st.text_input("Title", placeholder="My reflection for today…")
            j_content = st.text_area("Content", placeholder="Write your thoughts…", height=130)
            j_mood    = st.selectbox("Mood", MOODS)
            if st.form_submit_button("💾 Save entry"):
                if not j_title.strip() or not j_content.strip():
                    st.error("Title and content are required.")
                else:
                    r = requests.post(f"{BASE_URL}/journal",
                                      json={"title": j_title, "content": j_content, "mood": j_mood})
                    st.success("Journal entry saved! 🌺") if r.status_code == 200 else st.error(r.text)

    with tab2:
        c1, c2 = st.columns(2)
        with c1: filter_mood = st.selectbox("Filter by mood", ["All"] + MOODS)
        with c2: filter_days = st.selectbox("Filter by period", ["All time", "Last 7 days", "Last 30 days"])

        params = {}
        if filter_mood != "All":          params["mood"] = filter_mood
        if filter_days == "Last 7 days":  params["days"] = 7
        elif filter_days == "Last 30 days": params["days"] = 30

        r = requests.get(f"{BASE_URL}/journal", params=params)
        if r.status_code == 200:
            journals = r.json()
            if not journals:
                st.info("No journal entries found.")
            else:
                for j in journals:
                    me = MOOD_EMOJI.get(j["mood"], "📝")
                    dt = datetime.fromisoformat(j["created_at"]).strftime("%d %b %Y, %I:%M %p")
                    with st.expander(f"{me}  {j['title']}  ·  {j['mood']}  ·  {dt}"):
                        st.write(j["content"])
                        if st.button(f"🗑 Delete #{j['id']}", key=f"del_{j['id']}"):
                            rd = requests.delete(f"{BASE_URL}/journal/{j['id']}")
                            st.success("Deleted!") if rd.status_code == 200 else st.error(rd.text)
                            if rd.status_code == 200: st.rerun()

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            r_s = requests.get(f"{BASE_URL}/journal/stats/streak")
            if r_s.status_code == 200:
                st.metric("🔥 Current streak", f"{r_s.json().get('current_streak', 0)} days")
        with c2:
            r_t = requests.get(f"{BASE_URL}/journal/stats/top-moods")
            if r_t.status_code == 200:
                top_data = r_t.json()
                if "top_moods" in top_data and top_data["top_moods"]:
                    top = top_data["top_moods"][0]
                    st.metric("💫 Top mood", f"{top['mood']} ({top['count']}×)")

        section_card("Mood breakdown")
        r_stats = requests.get(f"{BASE_URL}/journal/stats")
        if r_stats.status_code == 200:
            stats = r_stats.json()
            if stats:
                for s in stats:
                    me  = MOOD_EMOJI.get(s["mood"], "📝")
                    bar = "█" * min(s["count"], 20)
                    st.markdown(
                        f'<div style="margin:5px 0; color:#c8b8e8; font-size:13px;">'
                        f'{me} <b>{s["mood"]}</b> '
                        f'<span style="color:rgba(200,168,75,0.6);">{bar}</span> '
                        f'<span style="color:#c8a84b;">({s["count"]})</span></div>',
                        unsafe_allow_html=True
                    )
            else:
                st.info("No stats yet.")


# ═══════════════════════════════════════════════════════════════════════════════
# MORNING ROUTINE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🌅  Morning Routine":
    st.markdown("# 🌅 Morning Routine")
    st.markdown('<p style="color:rgba(200,168,75,0.65); font-size:13px;">Track your sacred morning practices.</p>', unsafe_allow_html=True)

    tab_log, tab_hist = st.tabs(["📋  Log today", "📅  History"])

    with tab_log:
        r_today  = requests.get(f"{BASE_URL}/morning-routine/{date.today()}")
        existing = r_today.json() if r_today.status_code == 200 else None
        dv = lambda k: existing[k] if existing else False

        st.markdown(f'<p style="color:rgba(200,168,75,0.7); font-size:13px;">{date.today().strftime("%A, %d %B %Y")}</p>', unsafe_allow_html=True)

        with st.form("morning_form"):
            c1, c2 = st.columns(2)
            with c1:
                walk  = st.checkbox("🚶 Morning Walk",        value=dv("walk"))
                yoga  = st.checkbox("🧘 Yoga",                value=dv("yoga"))
                surya = st.checkbox("☀️ Surya Arghya",        value=dv("surya_arghya"))
            with c2:
                shiva  = st.checkbox("💧 Shiva Jal",          value=dv("shiva_jal"))
                vishnu = st.checkbox("📿 Vishnu Sahasranamam", value=dv("vishnu_sahasranamam"))

            btn_label = "🔄 Update routine" if existing else "💾 Save routine"
            if st.form_submit_button(btn_label):
                payload = {"walk": walk, "yoga": yoga, "surya_arghya": surya,
                           "shiva_jal": shiva, "vishnu_sahasranamam": vishnu}
                if existing:
                    rr = requests.patch(f"{BASE_URL}/morning-routine/{date.today()}", json=payload)
                else:
                    payload["date"] = str(date.today())
                    rr = requests.post(f"{BASE_URL}/morning-routine", json=payload)
                if rr.status_code == 200:
                    st.success("Routine saved! 🌺")
                    st.rerun()
                else:
                    st.error(rr.text)

        if existing:
            done = sum([existing["walk"], existing["yoga"], existing["surya_arghya"],
                        existing["shiva_jal"], existing["vishnu_sahasranamam"]])
            st.progress(done / 5, text=f"✅ {done}/5 practices completed today")

    with tab_hist:
        r_all = requests.get(f"{BASE_URL}/morning-routine")
        if r_all.status_code == 200:
            routines = r_all.json()
            if not routines:
                st.info("No routines logged yet.")
            else:
                for rt in routines:
                    done = sum([rt["walk"], rt["yoga"], rt["surya_arghya"],
                                rt["shiva_jal"], rt["vishnu_sahasranamam"]])
                    with st.expander(f"📅 {rt['date']}  —  {done}/5 ✅"):
                        for key, label in [
                            ("walk", "🚶 Walk"), ("yoga", "🧘 Yoga"),
                            ("surya_arghya", "☀️ Surya Arghya"),
                            ("shiva_jal", "💧 Shiva Jal"),
                            ("vishnu_sahasranamam", "📿 Vishnu Sahasranamam")
                        ]:
                            icon = "✅" if rt[key] else "⭕"
                            st.markdown(f"{icon} {label}")


# ═══════════════════════════════════════════════════════════════════════════════
# SANKALP
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📿  Sankalp":
    st.markdown("# 📿 Daily Sankalp")
    st.markdown('<p style="color:rgba(200,168,75,0.65); font-size:13px;">One sacred intention — one day at a time.</p>', unsafe_allow_html=True)

    tab_new, tab_all = st.tabs(["🌸  Today", "📜  All Sankalps"])

    with tab_new:
        r_today = requests.get(f"{BASE_URL}/sankalp/{date.today()}")
        if r_today.status_code == 200:
            s = r_today.json()
            st.markdown(
                f'<div class="soul-card">'
                f'<div style="font-size:10px; text-transform:uppercase; letter-spacing:0.1em; '
                f'color:rgba(200,168,75,0.55); margin-bottom:8px;">Today\'s Sankalp</div>'
                f'<p style="font-size:15px; font-style:italic; color:#fff; '
                f'line-height:1.6; margin:0;">"{s["sankalp"]}"</p></div>',
                unsafe_allow_html=True
            )
            st.info("✅ Today's Sankalp is already set.")
        else:
            with st.form("sankalp_form", clear_on_submit=True):
                sankalp_text = st.text_area(
                    "Your Sankalp for today",
                    placeholder="Today I will be patient and present…",
                    height=100
                )
                if st.form_submit_button("💫 Set Sankalp"):
                    if not sankalp_text.strip():
                        st.error("Please enter a Sankalp.")
                    else:
                        r = requests.post(f"{BASE_URL}/sankalp",
                                          json={"date": str(date.today()), "sankalp": sankalp_text})
                        if r.status_code == 200:
                            st.success("Sankalp saved! 🌺")
                            st.rerun()
                        elif r.status_code == 400:
                            st.warning("Today's Sankalp already exists.")
                        else:
                            st.error(r.text)

    with tab_all:
        r = requests.get(f"{BASE_URL}/sankalp")
        if r.status_code == 200:
            sankalps = r.json()
            if not sankalps:
                st.info("No Sankalps yet.")
            else:
                for s in sankalps:
                    f_icon  = "✅" if s.get("fulfilled") else ("❌" if s.get("fulfilled") is False else "🔄")
                    preview = s["sankalp"][:60] + ("…" if len(s["sankalp"]) > 60 else "")
                    with st.expander(f"📅 {s['date']}  {f_icon}  —  {preview}"):
                        st.markdown(f"**Sankalp:** {s['sankalp']}")
                        if s.get("reflection"):
                            st.markdown(f"**Reflection:** {s['reflection']}")
                        if s.get("fulfilled") is not None:
                            st.markdown(f"**Fulfilled:** {'✅ Yes' if s['fulfilled'] else '❌ No'}")


# ═══════════════════════════════════════════════════════════════════════════════
# GRATITUDE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🙏  Gratitude":
    st.markdown("# 🙏 Gratitude Journal")
    st.markdown('<p style="color:rgba(200,168,75,0.65); font-size:13px;">A grateful heart is a magnet for miracles.</p>', unsafe_allow_html=True)

    with st.form("gratitude_form", clear_on_submit=True):
        grat_text = st.text_area(
            "What are you grateful for today?",
            placeholder="I am grateful for…",
            height=100
        )
        if st.form_submit_button("🙏 Save gratitude"):
            if not grat_text.strip():
                st.error("Please enter your gratitude.")
            else:
                r = requests.post(f"{BASE_URL}/gratitude", json={"gratitude": grat_text})
                if r.status_code == 200:
                    st.success("Gratitude saved! 🌺")
                    st.rerun()
                else:
                    st.error(r.text)

    section_card("All gratitude entries")
    r = requests.get(f"{BASE_URL}/gratitude")
    if r.status_code == 200:
        entries = r.json()
        if not entries:
            st.markdown('<div class="empty-state">🙏<br>No gratitude entries yet.<br>Start with one above!</div>', unsafe_allow_html=True)
        else:
            cols = st.columns(2)
            for i, item in enumerate(entries):
                with cols[i % 2]:
                    dt = datetime.fromisoformat(item["created_at"]).strftime("%d %b %Y, %I:%M %p")
                    st.markdown(
                        f'<div class="soul-card-accent">'
                        f'<p style="font-style:italic; color:#e8e0f0; font-size:13px; '
                        f'line-height:1.55; margin:0;">🙏 {item["gratitude"]}</p>'
                        f'<p style="font-size:10px; color:rgba(200,168,75,0.45); margin:5px 0 0;">{dt}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
