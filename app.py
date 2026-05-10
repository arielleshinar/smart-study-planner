import streamlit as st
from main import Task, create_schedule

st.set_page_config(page_title="Smart Study Planner", page_icon="📚", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #FDF6E3 !important;
    color: #3B2A1A !important;
  }

  .stApp {
    background-color: #FDF6E3 !important;
  }

  /* ── Hero header ── */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
  }

  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #3B2A1A;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
  }

  .hero p {
    font-size: 1.1rem;
    color: #7A5C3E;
    font-weight: 300;
    margin: 0;
  }

  .hero-line {
    width: 60px;
    height: 3px;
    background: #C4935A;
    margin: 1rem auto;
    border-radius: 2px;
  }

  /* ── Task cards ── */
  .task-card {
    background: #FFFBF0;
    border: 1px solid #E8D9B8;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 1rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(59,42,26,0.06);
  }

  .task-label {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 500;
    color: #C4935A;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
  }

  /* ── Inputs ── */
  input[type="text"], input[type="number"], .stTextInput input, .stNumberInput input {
    background: #FDF6E3 !important;
    border: 1px solid #D4B896 !important;
    border-radius: 10px !important;
    color: #3B2A1A !important;
    font-family: 'DM Sans', sans-serif !important;
  }

  input:focus {
    border-color: #C4935A !important;
    box-shadow: 0 0 0 2px rgba(196,147,90,0.2) !important;
  }

  label, .stTextInput label, .stNumberInput label {
    color: #7A5C3E !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
  }

  /* ── Button ── */
  .stButton > button {
    background: #3B2A1A !important;
    color: #FDF6E3 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
    transition: background 0.2s ease;
    width: 100%;
  }

  .stButton > button:hover {
    background: #5C3D22 !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background-color: #F5EDD6 !important;
    border-right: 1px solid #E8D9B8;
  }

  [data-testid="stSidebar"] * {
    color: #3B2A1A !important;
  }

  [data-testid="stSidebar"] .stCheckbox label {
    color: #3B2A1A !important;
    font-weight: 400 !important;
  }

  /* ── Schedule output ── */
  .day-card {
    background: #FFFBF0;
    border-left: 4px solid #C4935A;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
  }

  .day-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #3B2A1A;
    margin-bottom: 0.5rem;
  }

  .task-item {
    font-size: 0.9rem;
    color: #5C3D22;
    padding: 0.2rem 0;
  }

  .task-item span {
    font-weight: 500;
    color: #3B2A1A;
  }

  /* ── Section titles ── */
  .section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #3B2A1A;
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E8D9B8;
  }

  /* ── Info / warning banners ── */
  .stAlert {
    border-radius: 12px !important;
    border: 1px solid #E8D9B8 !important;
    background: #FFFBF0 !important;
    color: #3B2A1A !important;
  }

  /* ── Divider ── */
  hr {
    border-color: #E8D9B8 !important;
  }

  /* ── Expander ── */
  .streamlit-expanderHeader {
    background: #F5EDD6 !important;
    border-radius: 10px !important;
    color: #3B2A1A !important;
    font-weight: 500 !important;
  }

  /* ── Hide Streamlit branding ── */
  #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>Smart Study Planner</h1>
  <div class="hero-line"></div>
  <p>Build your perfect study schedule — balanced, realistic, and deadline-proof.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Settings")
    num_tasks = st.number_input("Number of tasks", min_value=1, step=1, value=2)
    max_hours = st.number_input("Daily study limit (hours)", min_value=1, step=1, value=4)
    auto_adjust = st.checkbox("Auto-adjust daily limit if needed")
    st.markdown("---")
    st.markdown("<small style='color:#7A5C3E'>Deadlines are in days from today.<br>Priority: 1 = low, 3 = urgent.</small>", unsafe_allow_html=True)

tasks = []

st.markdown('<div class="section-title">Your Tasks</div>', unsafe_allow_html=True)

for i in range(num_tasks):
    st.markdown(f'<div class="task-card"><div class="task-label">Task {i + 1}</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2.5, 1, 1, 1])

    with col1:
        name = st.text_input("Task name", key=f"name_{i}").strip()
    with col2:
        deadline = st.number_input("Deadline (days)", min_value=1, step=1, key=f"deadline_{i}")
    with col3:
        hours = st.number_input("Hours needed", min_value=1, step=1, key=f"hours_{i}")
    with col4:
        priority = st.number_input("Priority (1–3)", min_value=1, max_value=3, step=1, key=f"priority_{i}")

    if name:
        tasks.append(Task(name, deadline, hours, priority))

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Generate my schedule →", use_container_width=True):
    if tasks:
        schedule, messages, final_limit, needs_adjustment = create_schedule(
            tasks,
            max_hours_per_day=max_hours,
            auto_adjust=auto_adjust
        )

        failed = any("could not be fully scheduled" in msg for msg in messages)

        if failed:
            st.warning("Some tasks couldn't be fully scheduled within the daily limit.")

        if needs_adjustment and not auto_adjust:
            st.info("Tip: enable auto-adjust in the sidebar to find the minimum daily hours needed.")

        if messages:
            with st.expander("See details"):
                for msg in messages:
                    st.write(msg)

        st.markdown('<div class="section-title">Your Schedule</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#7A5C3E; font-size:0.9rem; margin-bottom:1.5rem'>Daily limit: <strong>{final_limit}h</strong></p>", unsafe_allow_html=True)

        if schedule:
            for day in sorted(schedule):
                items_html = "".join(
                    f'<div class="task-item">— <span>{task}</span> &nbsp;{hours}h</div>'
                    for task, hours in schedule[day]
                )
                st.markdown(f"""
                <div class="day-card">
                  <div class="day-title">Day {day}</div>
                  {items_html}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No schedule could be created with the current settings.")
    else:
        st.warning("Please enter at least one task name before generating.")