import streamlit as st
from main import Task, create_schedule

#display a big header in the browser
st.title("Smart Study Planner")

# creates a number input box in UI for number of tasks
num_tasks = st.number_input("Number of tasks", min_value=1, step=1)

tasks = []

# loop for each task
for i in range(num_tasks):
    # smaller headers for tasks - task 1, task 2, task 3...
    st.subheader(f"Task {i+1}")
    # name 1, name 2.... creates a text box and returns a string
    name = st.text_input(f"Name {i+1}")
    name = name.strip()
    # create numeric inputs and return numbers
    deadline = st.number_input(f"Deadline (days) {i+1}", min_value=1, step=1)
    hours = st.number_input(f"Hours needed {i+1}", min_value=1, step=1)
    priority = st.number_input(f"Priority (1-3) {i+1}", min_value=1, max_value=3, step=1)

    # only add task to the list if user actually typed a name
    if name:
        # creates a task object and adds it to the list
        tasks.append(Task(name, deadline, hours, priority))

# button to generate schedule. when user clicks becomes true, otherwise its false
# enter if user clicked the button
if st.button("Generate Schedule"):
    #if the list isn't empty
    if tasks:
        # call algorithm - now backend runs
        schedule = create_schedule(tasks)

        st.subheader("Schedule")

        # display schedule 
        # loop through days in order
        for day in sorted(schedule):
            # prints bold text
            st.write(f"**Day {day}**")
            # each day contains a list of ("task name", hours)
            for task, hours in schedule[day]:
                # displays each task nicely
                st.write(f"- {task}: {hours}h")
    # warns if there are no tasks
    else:
        st.warning("Please enter at least one task.")