import math
import urllib.parse
from datetime import date
import streamlit as st

st.set_page_config(page_title="Before You Build", page_icon="⚙️", layout="wide")

# HIGH-CONTRAST FUTURISTIC THEME
st.markdown("""
<style>
/* Main page */
.stApp {
    background: #07111F;
    color: #F8FAFC;
}
[data-testid="stAppViewContainer"] {
    background: #07111F;
}
[data-testid="stHeader"] {
    background: rgba(7, 17, 31, 0.95);
}
h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #67E8F9 !important;
    opacity: 1 !important;
}
p, li, .stMarkdown, [data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"], small {
    color: #F1F5F9 !important;
    opacity: 1 !important;
}
[data-testid="stCaptionContainer"] p {
    color: #D7E4F2 !important;
}

/* All form labels and widget labels */
label, .stTextInput label, .stTextArea label,
.stNumberInput label, .stSelectbox label,
.stMultiSelect label, .stRadio label,
.stCheckbox label, .stSlider label,
[data-testid="stWidgetLabel"] *,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Text, number and text-area fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    color: #FFFFFF !important;
    background: #142943 !important;
    border: 1px solid #6B8BAA !important;
    border-radius: 8px !important;
    caret-color: #67E8F9 !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #C7D7E8 !important;
    -webkit-text-fill-color: #C7D7E8 !important;
    opacity: 1 !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border: 2px solid #67E8F9 !important;
    box-shadow: 0 0 0 2px rgba(103, 232, 249, 0.18) !important;
}

/* Select boxes and multiselect */
div[data-baseweb="select"] > div {
    background: #142943 !important;
    border: 1px solid #6B8BAA !important;
    color: #FFFFFF !important;
}
div[data-baseweb="select"] *,
div[data-baseweb="select"] input,
div[data-baseweb="select"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background: #142943 !important;
}
li[role="option"], li[role="option"] *,
div[role="option"], div[role="option"] * {
    color: #FFFFFF !important;
    background: #142943 !important;
}
li[role="option"]:hover,
div[role="option"]:hover {
    background: #245078 !important;
}

/* Sidebar navigation */
section[data-testid="stSidebar"] {
    background: #101F33 !important;
    border-right: 1px solid #35516D !important;
}
section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
    opacity: 1 !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: #172B43 !important;
    border: 1px solid #36536F !important;
    border-radius: 8px !important;
    padding: 8px 10px !important;
    margin-bottom: 5px !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #23496A !important;
}

/* Metric cards: cost, budget, time */
[data-testid="stMetric"] {
    background: #142943 !important;
    border: 1px solid #5B7D9E !important;
    padding: 18px !important;
    border-radius: 12px !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* Buttons */
.stButton button, .stFormSubmitButton button,
.stDownloadButton button, .stLinkButton a {
    background: #087FAE !important;
    color: #FFFFFF !important;
    border: 1px solid #67E8F9 !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
}
.stButton button *, .stFormSubmitButton button *,
.stDownloadButton button *, .stLinkButton a * {
    color: #FFFFFF !important;
}
.stButton button:hover, .stFormSubmitButton button:hover,
.stDownloadButton button:hover, .stLinkButton a:hover {
    background: #0B98C9 !important;
    border-color: #FFFFFF !important;
}

/* Alerts and status messages */
[data-testid="stAlert"] {
    border: 1px solid #7896B3 !important;
    border-radius: 9px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Expanders, tabs and general containers */
[data-testid="stExpander"] {
    background: #12263D !important;
    border: 1px solid #55728F !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary *,
.stTabs [role="tab"],
.stTabs [role="tab"] * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
    color: #67E8F9 !important;
    border-bottom-color: #67E8F9 !important;
}

/* Dividers and progress elements */
hr {
    border-color: #45627E !important;
}
.stProgress > div > div {
    background: #22B8D6 !important;
}

/* Keep disabled/read-only text readable too */
input:disabled, textarea:disabled {
    color: #DCE8F5 !important;
    -webkit-text-fill-color: #DCE8F5 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

C = {
    "Arduino Uno": (450, 2), "Arduino Nano": (300, 2),
    "Ultrasonic Sensor": (120, 1), "IR Sensor": (80, 1),
    "Servo Motor": (180, 2), "DC Motor": (150, 2),
    "LED": (10, .5), "Breadboard": (100, .5),
    "Jumper Wires": (60, .5), "Battery": (150, 1),
    "LCD Display": (200, 2), "OLED Display": (250, 2),
    "Relay Module": (100, 1), "Temperature Sensor": (130, 1),
    "Soil Moisture Sensor": (100, 1), "ESP32": (400, 2)
}
BASE = {"Robotics": 5, "IoT": 4, "Automation": 4, "Smart Systems": 3, "Other": 3}
MULT = {"Beginner": 1, "Intermediate": 1.5, "Advanced": 2}
RISKS = [
    ({"DC Motor", "Servo Motor"}, "Motor power: make sure the supply can drive the motors."),
    ({"Arduino Uno", "Arduino Nano"}, "Controller limits: check pins and memory."),
    ({"ESP32"}, "Wireless setup may need extra testing."),
    ({"Battery"}, "Power management: check voltage/current of every part.")
]
STAGES = [
    "Research and problem identification", "Concept design and planning",
    "Component procurement", "Prototype assembly", "Programming and integration",
    "Testing and debugging", "Final improvements"
]

for k, v in dict(
    idea="", purpose="", category="Robotics", budget=2000, team=1,
    hours=4, level="Beginner", sel=[], qty={}
).items():
    st.session_state.setdefault(k, v)
S = st.session_state


def calc():
    cost = sum(C[i][0] * S.qty.get(i, 1) for i in S.sel)
    work = sum(C[i][1] * S.qty.get(i, 1) for i in S.sel)
    h = math.ceil((BASE[S.category] + work) * MULT[S.level])
    return dict(
        cost=cost, left=S.budget - cost, ok=cost <= S.budget,
        hours=h, days=math.ceil(h / (S.team * S.hours))
    )


def risks():
    return [m for t, m in RISKS if t & set(S.sel)] + [
        "Testing: allow extra time for debugging."
    ]


page = st.sidebar.radio(
    "⚙️ BEFORE YOU BUILD",
    ["Dashboard", "Idea Lab", "Component Lab", "Cost & Time",
     "Procurement", "Feasibility", "Roadmap", "Report"]
)

if page == "Dashboard":
    st.title("⚙️ BEFORE YOU BUILD")
    st.subheader("Think. Simulate. Build.")
    st.write(
        "Plan your engineering project before you build it: ideas, components, "
        "cost, time, risks, shopping links and a downloadable report."
    )
    if S.idea:
        st.success(f"Current project: {S.idea}")
    else:
        st.warning("No project yet. Start in Idea Lab.")
    st.stop()

if page == "Idea Lab":
    st.title("💡 IDEA LAB")
    st.write("Start by naming your project and describing the problem you want to solve.")
    with st.form("f"):
        idea = st.text_input(
            "Project Name",
            value=S.idea,
            placeholder="Write your project name here..."
        )
        purpose = st.text_area(
            "Project Topic / Problem",
            value=S.purpose,
            placeholder="Enter your project topic and explain what problem it solves..."
        )
        cat = st.selectbox("Category", list(BASE), list(BASE).index(S.category))
        budget = st.number_input("Estimated Budget (₹)", 100, 100000, S.budget, 100)
        level = st.selectbox("Difficulty", list(MULT), list(MULT).index(S.level))
        team = st.number_input("Team members", 1, 20, S.team)
        hrs = st.number_input("Hours per person per day", 1, 12, S.hours)
        if st.form_submit_button("SAVE PROJECT DETAILS"):
            if idea.strip() and purpose.strip():
                S.update(
                    idea=idea, purpose=purpose, category=cat, budget=budget,
                    level=level, team=team, hours=hrs
                )
                st.success("Project details saved!")
            else:
                st.error("Please enter both your project name and project topic.")
    st.stop()

if page == "Component Lab":
    st.title("🔧 COMPONENT LAB")
    st.write("Choose the components you plan to use in your project.")
    st.caption("Select one or more components. You can adjust the quantity of each below.")
    S.sel = st.multiselect(
        "Select project components",
        list(C),
        [x for x in S.sel if x in C]
    )
    for i in S.sel:
        S.qty[i] = st.number_input(
            f"{i} — ₹{C[i][0]} each", 1, 100, S.qty.get(i, 1), key=f"q_{i}"
        )
    if S.sel:
        st.metric("Estimated Component Cost", f"₹{calc()['cost']}")
    st.stop()

if not S.idea or not S.sel:
    st.warning("Save a project in Idea Lab and pick components in Component Lab first.")
    st.stop()

r = calc()

if page == "Cost & Time":
    st.title("📊 COST & TIME")
    a, b, c = st.columns(3)
    a.metric("Estimated Cost", f"₹{r['cost']}")
    b.metric("Estimated Budget", f"₹{S.budget}")
    c.metric("Remaining Budget", f"₹{r['left']}")
    a, b = st.columns(2)
    a.metric("Estimated Man-Hours", f"{r['hours']} h")
    b.metric("Estimated Completion", f"{r['days']} days")
    st.caption("Preliminary rule-based estimates, not guaranteed.")

elif page == "Procurement":
    st.title("🛒 PROCUREMENT")
    for i in S.sel:
        q = urllib.parse.quote_plus(i)
        st.subheader(i)
        st.write(f"₹{C[i][0]} | Qty: {S.qty.get(i, 1)}")
        a, b = st.columns(2)
        a.link_button("Amazon", f"https://www.amazon.in/s?k={q}", use_container_width=True)
        b.link_button("Flipkart", f"https://www.flipkart.com/search?q={q}", use_container_width=True)
    st.caption("Verify prices and availability on the shopping sites.")

elif page == "Feasibility":
    st.title("📊 FEASIBILITY & RISK")
    (st.success if r["ok"] else st.error)(
        "Within budget." if r["ok"] else "Cost exceeds budget."
    )
    for x in risks():
        st.warning(x)
    st.caption("Preliminary assessment, not a safety certification.")

elif page == "Roadmap":
    st.title(f"📅 ROADMAP: {S.idea}")
    for i, s in enumerate(STAGES, 1):
        with st.expander(f"Stage {i}"):
            st.write(s)
    st.success(f"Estimated completion: {r['days']} days")

elif page == "Report":
    st.title("📄 REPORT")
    parts = "\n".join(
        f"- {i}: {S.qty.get(i, 1)} x Rs. {C[i][0]}" for i in S.sel
    )
    report = f"""BEFORE YOU BUILD - PROJECT REPORT
Project: {S.idea} | {S.category} | {S.level}
Purpose: {S.purpose}

COMPONENTS
{parts}

Cost: Rs. {r['cost']} | Budget: Rs. {S.budget} | Remaining: Rs. {r['left']}
Status: {"Within budget" if r['ok'] else "Exceeds budget"}
Man-hours: {r['hours']} | Completion: {r['days']} days

RISKS
""" + "\n".join(f"- {x}" for x in risks()) + f"""

All values are illustrative estimates. Generated on {date.today()}
"""
    st.download_button(
        "DOWNLOAD REPORT", report, "report.txt", use_container_width=True
    )
