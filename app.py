import streamlit as st
from main import Task, create_schedule

st.set_page_config(page_title="Smart Study Planner", page_icon="📚", layout="wide")

st.title("Smart Study Planner")
st.write("Build an optimized study plan based on deadlines, workload, and priority.")

# Everything inside this block appears in the sidebar instead of the main page
with st.sidebar:
    st.header("Settings")
    num_tasks = st.number_input("Number of tasks", min_value=1, step=1)
    # if checked auto_adjust=true, else its false
    auto_adjust = st.checkbox("Automatically increase daily limit if needed")

# create an empty list we'll fill with task objects based on what the user enters
tasks = []

# loop runs once for each task the user wants
for i in range(num_tasks):
    # st.markdown supports markdown formatting, and ### means a level-3 heading
    st.markdown(f"### Task {i+1}")
    # name column is wider than 3 number input columns
    col1, col2, col3, col4 = st.columns([2.5, 1, 1, 1])

    # anything inside with col1: appears in the first column
    with col1:
        name = st.text_input("Task Name", key=f"name_{i}").strip()

    with col2:
        deadline = st.number_input("Deadline", min_value=1, step=1, key=f"deadline_{i}")

    with col3:
        hours = st.number_input("Hours Needed", min_value=1, step=1, key=f"hours_{i}")

    with col4:
        priority = st.number_input("Priority", min_value=1, max_value=3, step=1, key=f"priority_{i}")

    # makes sure the task has a valid name (not only white spaces)
    if name:
        # if the name is valid we create a task object and add it to the list
        tasks.append(Task(name, deadline, hours, priority))

    # adds horizontal line after each task block to visually seperate tasks
    st.divider()

# this block only runs after the button is pressed
if st.button("Generate Schedule", use_container_width=True):
    # make sure at least 1 valid task exists
    if tasks:
        # call backend scheduling logic
        schedule, messages, final_limit, needs_adjustment = create_schedule(
            tasks,
            auto_adjust=auto_adjust
        )

        # detects if any task failed - even if only one did failed = true
        failed = any("could not be fully scheduled" in msg for msg in messages)

        # if task failed show one summary warning
        if failed:
            st.warning("Some tasks could not be fully scheduled with the current daily limit.")

        # shows blue suggestion only when schedule needs adjustment but the user didn't enable auto-adjust
        if needs_adjustment and not auto_adjust:
            st.info("Turn on auto-adjust to use the minimum daily limit needed for a feasible schedule.")

        # only shows the details section if there are messages
        if messages:
            # creates a collapsable section
            with st.expander("See details"):
                # loops through all backend messages
                for msg in messages:
                    # Displays each message inside the expander
                    st.write(msg)

        # ------ shcedule section -------
        st.subheader("Schedule")
        # shows the final daily limit that we used
        st.write(f"**Daily limit used:** {final_limit}h")

        # shows schedule if one exists
        if schedule:
            for day in sorted(schedule):
                # creates a grouped section for each day
                with st.container():
                    # displays a days heading
                    st.markdown(f"### Day {day}")
                    for task, hours in schedule[day]:
                        # Displays each scheduled item as a bullet point with the task name bolded
                        st.markdown(f"- **{task}** — {hours}h")
                    # adds a line after each day section
                    st.divider()
        
        # if the schedule dictionary is empty show a blue info message instead
        else:
            st.info("No schedule could be created.")
    
    # fallback if the user clicked the button without entering any valid task names
    else:
        st.warning("Please enter at least one valid task.")