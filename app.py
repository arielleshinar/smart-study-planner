import streamlit as st
from main import Task, create_schedule

st.title("Smart Study Planner")

num_tasks = st.number_input("Number of tasks", min_value=1, step=1)

tasks = []

for i in range(num_tasks):
    st.subheader(f"Task {i+1}")

    name = st.text_input(f"Name {i+1}", key=f"name_{i}").strip()
    deadline = st.number_input(
        f"Deadline (days) {i+1}",
        min_value=1,
        step=1,
        key=f"deadline_{i}"
    )
    hours = st.number_input(
        f"Hours needed {i+1}",
        min_value=1,
        step=1,
        key=f"hours_{i}"
    )
    priority = st.number_input(
        f"Priority (1-3) {i+1}",
        min_value=1,
        max_value=3,
        step=1,
        key=f"priority_{i}"
    )

    if name:
        tasks.append(Task(name, deadline, hours, priority))

auto_adjust = st.checkbox("Automatically increase daily limit if needed")

if st.button("Generate Schedule"):
    if tasks:
        schedule, messages, final_limit, needs_adjustment = create_schedule(
            tasks,
            auto_adjust=auto_adjust
        )

        failed = any("could not be fully scheduled" in msg for msg in messages)

        if failed:
            st.warning("Some tasks could not be fully scheduled with the current daily limit.")

        if needs_adjustment and not auto_adjust:
            st.info("Turn on auto-adjust to use the minimum daily limit needed for a feasible schedule.")

        if messages:
            with st.expander("See details"):
                for msg in messages:
                    st.write(msg)

        st.subheader("Schedule")
        st.write(f"**Daily limit used:** {final_limit}h")

        if schedule:
            for day in sorted(schedule):
                st.write(f"**Day {day}**")
                for task, hours in schedule[day]:
                    st.write(f"• {task} — {hours}h")
        else:
            st.info("No schedule could be created.")
    else:
        st.warning("Please enter at least one valid task.")