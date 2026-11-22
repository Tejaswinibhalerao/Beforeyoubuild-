import math
import json
import urllib.parse
from pathlib import Path
from datetime import date
import streamlit as st

st.set_page_config(page_title="Before You Build", page_icon="⚙️", layout="wide")

# HIGH-CONTRAST FUTURISTIC THEME
st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"] { background:#07111F !important; color:#F8FAFC !important; }
[data-testid="stHeader"] { background:rgba(7,17,31,.96) !important; }
h1,h2,h3,h4,h5,h6 { color:#67E8F9 !important; opacity:1 !important; }
p,li,small,[data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] { color:#F1F5F9 !important; opacity:1 !important; }
[data-testid="stCaptionContainer"] p { color:#DCE8F5 !important; }
label,[data-testid="stWidgetLabel"],[data-testid="stWidgetLabel"] * { color:#FFFFFF !important; font-weight:700 !important; opacity:1 !important; }
/* Text inputs: target Streamlit and BaseWeb wrappers to prevent pale text on pale fields. */
.stTextInput input,.stTextArea textarea,.stNumberInput input,
[data-baseweb="input"] input,[data-baseweb="textarea"] textarea,
[data-testid="stDateInput"] input,[data-testid="stTimeInput"] input {
  background:#F8FAFC !important; color:#111827 !important;
  -webkit-text-fill-color:#111827 !important; caret-color:#087FAE !important;
  border:1px solid #64748B !important; border-radius:8px !important; opacity:1 !important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder,
[data-baseweb="input"] input::placeholder,[data-baseweb="textarea"] textarea::placeholder {
  color:#475569 !important; -webkit-text-fill-color:#475569 !important; opacity:1 !important;
}
/* Selects and dropdown choices */
div[data-baseweb="select"] > div { background:#F8FAFC !important; border:1px solid #64748B !important; }
div[data-baseweb="select"] *,div[data-baseweb="select"] input,
div[data-baseweb="select"] span { color:#111827 !important; -webkit-text-fill-color:#111827 !important; }
div[data-baseweb="popover"],div[data-baseweb="menu"],ul[role="listbox"] { background:#FFFFFF !important; }
li[role="option"],li[role="option"] *,div[role="option"],div[role="option"] * { color:#111827 !important; background:#FFFFFF !important; }
li[role="option"]:hover,div[role="option"]:hover { background:#DBEAFE !important; }
section[data-testid="stSidebar"] { background:#101F33 !important; border-right:1px solid #35516D !important; }
section[data-testid="stSidebar"] * { color:#F8FAFC !important; opacity:1 !important; }
section[data-testid="stSidebar"] [role="radiogroup"] label { background:#172B43 !important; border:1px solid #36536F !important; border-radius:8px !important; padding:8px 10px !important; margin-bottom:5px !important; }
[data-testid="stMetric"] { background:#142943 !important; border:1px solid #5B7D9E !important; padding:18px !important; border-radius:12px !important; }
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] *,[data-testid="stMetricValue"],[data-testid="stMetricValue"] * { color:#FFFFFF !important; -webkit-text-fill-color:#FFFFFF !important; opacity:1 !important; font-weight:800 !important; }
.stButton button,.stFormSubmitButton button,.stDownloadButton button,.stLinkButton a { background:#087FAE !important; color:#FFFFFF !important; border:1px solid #67E8F9 !important; border-radius:9px !important; font-weight:800 !important; }
.stButton button *,.stFormSubmitButton button *,.stDownloadButton button *,.stLinkButton a * { color:#FFFFFF !important; }
[data-testid="stAlert"] { border:1px solid #7896B3 !important; border-radius:9px !important; }
[data-testid="stAlert"] p,[data-testid="stAlert"] div,[data-testid="stAlert"] span { color:#FFFFFF !important; opacity:1 !important; }
[data-testid="stExpander"] { background:#12263D !important; border:1px solid #55728F !important; border-radius:10px !important; }
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *, .stTabs [role="tab"],.stTabs [role="tab"] * { color:#FFFFFF !important; font-weight:700 !important; }
hr { border-color:#45627E !important; }
.stProgress > div > div { background:#22B8D6 !important; }
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

# Local autosave file. This preserves the prototype data across page changes and app restarts
# on the same persistent server. Downloadable backups are also provided in the app.
SAVE_FILE = Path("before_you_build_data.json")
DEFAULTS = dict(
    idea="", purpose="", category="Robotics", budget=2000, team=1,
    hours=4, level="Beginner", sel=[], qty={}, project_saved=False
)
if "_loaded_saved_data" not in st.session_state:
    if SAVE_FILE.exists():
        try:
            saved = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
            for key, value in saved.items():
                if key in DEFAULTS:
                    DEFAULTS[key] = value
        except (OSError, json.JSONDecodeError):
            pass
    st.session_state["_loaded_saved_data"] = True
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
S = st.session_state

def save_project_data():
    data = {key: S.get(key, value) for key, value in DEFAULTS.items()}
    try:
        SAVE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except OSError:
        return False

def show_save_status():
    """Persistent status banner, visible every time the page is opened."""
    if S.project_saved and S.idea.strip():
        st.success(f"✓ PROJECT SAVED: {S.idea}")
    else:
        st.info("NO PROJECT SAVED YET — complete the Idea Lab and press SAVE PROJECT DETAILS.")


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
    st.write("Plan your engineering project before you build it: ideas, components, cost, time, risks, shopping links and a downloadable report.")
    st.markdown("### PROJECT STATUS")
    show_save_status()
    if S.project_saved and S.idea.strip():
        st.markdown(f"### {S.idea}")
        st.write(f"**Project topic:** {S.purpose}")
        a, b, c = st.columns(3)
        a.metric("Category", S.category)
        b.metric("Estimated Budget", f"₹{S.budget:,}")
        c.metric("Components Selected", len(S.sel))
        if S.sel:
            st.write("**Selected components:** " + ", ".join(S.sel))
        else:
            st.info("Your project is saved. Select components in Component Lab to calculate cost and time.")
    else:
        st.warning("Your project will appear here after you save it in Idea Lab.")
    st.caption("Keep a downloadable backup from the Report section. Local file persistence depends on the hosting environment.")
    if st.button("SAVE CURRENT PROJECT NOW", use_container_width=True):
        if save_project_data(): st.success("Project data saved successfully.")
        else: st.error("Could not write the local save file. Download a backup from Report.")
    st.stop()

if page == "Idea Lab":
    st.title("💡 IDEA LAB")
    show_save_status()
    if S.project_saved and S.idea.strip():
        st.info(f"Saved project: {S.idea}  |  Topic: {S.purpose}")
    st.write("Start by naming your project and describing the problem you want to solve.")
    with st.form("idea_form"):
        idea = st.text_input("Project Name", value=S.idea, placeholder="Write your project name here...")
        purpose = st.text_area("Project Topic / Problem", value=S.purpose, placeholder="Enter your project topic and explain what problem it solves...")
        cat = st.selectbox("Category", list(BASE), index=list(BASE).index(S.category) if S.category in BASE else 0)
        budget = st.number_input("Estimated Budget (₹)", 100, 100000, int(S.budget), 100)
        level = st.selectbox("Difficulty", list(MULT), index=list(MULT).index(S.level) if S.level in MULT else 0)
        team = st.number_input("Team members", 1, 20, int(S.team))
        hrs = st.number_input("Hours per person per day", 1, 12, int(S.hours))
        submitted = st.form_submit_button("SAVE PROJECT DETAILS", use_container_width=True)
    if submitted:
        if idea.strip() and purpose.strip():
            S.update(idea=idea.strip(), purpose=purpose.strip(), category=cat, budget=budget, level=level, team=team, hours=hrs, project_saved=True)
            if save_project_data():
                st.success("✓ PROJECT SAVED SUCCESSFULLY — it is now displayed on your Dashboard.")
            else:
                st.warning("Project saved for this session, but local autosave failed. Download a backup from Report.")
        else:
            st.error("Please enter both your project name and project topic.")
    st.stop()

if page == "Component Lab":
    st.title("🔧 COMPONENT LAB")
    show_save_status()
    st.write("Choose the components you plan to use in your project.")
    st.caption("Select one or more components. You can adjust the quantity of each below.")
    selected = st.multiselect("Select project components", list(C), [x for x in S.sel if x in C])
    S.sel = selected
    for item in S.sel:
        S.qty[item] = st.number_input(f"{item} — ₹{C[item][0]} each", 1, 100, int(S.qty.get(item, 1)), key=f"q_{item}")
    if S.sel:
        st.metric("Estimated Component Cost", f"₹{calc()['cost']:,}")
    if save_project_data():
        st.caption("✓ Component selections and quantities autosaved.")
    st.stop()

# Feasibility is intentionally available even before components are selected.
# Other calculation pages need a saved idea and at least one selected component.
if page != "Feasibility" and (not S.idea.strip() or not S.sel):
    st.title(page.upper())
    show_save_status()
    st.info("Save your project in Idea Lab and select at least one component in Component Lab to view this section.")
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
    show_save_status()
    if not S.idea.strip():
        st.info("Save a project in Idea Lab to personalize this assessment. You can still view the preliminary checklist below.")
    if not S.sel:
        st.warning("No components selected yet. This is a preliminary assessment; select components in Component Lab for a detailed cost and component-risk check.")
        a, b, c = st.columns(3)
        a.metric("Project Details", "Saved" if S.project_saved and S.idea.strip() else "Pending")
        b.metric("Components", "Not selected")
        c.metric("Budget", f"₹{S.budget:,}" if S.project_saved else "Not set")
        st.markdown("### INITIAL FEASIBILITY CHECKLIST")
        st.write("**Technical feasibility:** Confirm that the required components and tools are available.")
        st.write("**Budget feasibility:** List expected component, assembly and testing expenses before purchasing.")
        st.write("**Time feasibility:** Reserve time for research, assembly, testing and improvements.")
        st.write("**Team feasibility:** Divide research, design, assembly and documentation tasks among team members.")
        st.write("**Risk management:** Check component compatibility, power requirements and safe lab procedures with your instructor.")
    else:
        a, b, c = st.columns(3)
        a.metric("Estimated Cost", f"₹{r['cost']:,}")
        b.metric("Available Budget", f"₹{S.budget:,}")
        c.metric("Budget Remaining", f"₹{r['left']:,}")
        (st.success if r["ok"] else st.error)("Within budget." if r["ok"] else "Cost exceeds budget.")
        st.markdown("### COMPONENT-BASED RISKS")
        for risk in risks():
            st.warning(risk)
        st.markdown("### FEASIBILITY CHECKLIST")
        st.write("**Technical feasibility:** Review controller capacity and component compatibility.")
        st.write("**Budget feasibility:** Compare the estimated cost with the available budget.")
        st.write("**Time feasibility:** Estimated completion is " + str(r["days"]) + " days based on the team size and daily work hours.")
        st.write("**Team feasibility:** Assign clear responsibilities for design, assembly, testing and documentation.")
    st.caption("This is a preliminary planning assessment, not a safety certification. Follow your institution's laboratory instructions.")

elif page == "Roadmap":
    st.title(f"📅 ROADMAP: {S.idea}")
    for i, s in enumerate(STAGES, 1):
        with st.expander(f"Stage {i}"):
            st.write(s)
    st.success(f"Estimated completion: {r['days']} days")

elif page == "Report":
    st.title("📄 REPORT")
    show_save_status()
    backup = {key: S.get(key, value) for key, value in DEFAULTS.items()}
    st.download_button(
        "DOWNLOAD PROJECT BACKUP (JSON)",
        json.dumps(backup, indent=2),
        "before_you_build_backup.json",
        mime="application/json",
        use_container_width=True
    )
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
