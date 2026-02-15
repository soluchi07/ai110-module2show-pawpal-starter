import streamlit as st

from pawpal_system import Task, Pet, PetOwner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_type = st.selectbox("Task type", ["walk", "feed", "groom", "play", "other"], key="task_type_select")
task_notes = st.text_area("Notes (optional)", value="")

if st.button("Add task"):
    task = Task(
        title=task_title,
        task_type=task_type,
        duration_minutes=int(duration),
        priority=priority,
        notes=task_notes
    )
    if st.session_state.scheduler.add_task(task):
        st.success(f"Added task: {task.title}")
    else:
        st.error("Invalid task. Please check the inputs.")

if st.session_state.scheduler.tasks:
    st.write("Current tasks:")
    task_display_data = [
        {
            "Title": t.title,
            "Type": t.task_type,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Notes": t.notes if t.notes else "—"
        }
        for t in st.session_state.scheduler.tasks
    ]
    st.table(task_display_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily plan for your pet based on your tasks and availability.")

if st.button("Generate schedule"):
    if not st.session_state.scheduler.tasks:
        st.error("No tasks added. Please add at least one task above.")
    else:
        scheduler = st.session_state.scheduler

        # Create and add pet
        pet = Pet(name=pet_name, species=species)
        scheduler.set_pet(pet)

        # Set owner and availability (default: 8am to 10pm = 480 to 1320 minutes)
        owner = PetOwner(name=owner_name, availability=(480, 1320))
        scheduler.set_owner(owner)
        
        # Generate plan
        plan = scheduler.generate_plan()
        
        if plan:
            st.success(f"Schedule generated for {pet_name}!")
            st.markdown(f"**Plan for {pet_name} ({species})**")
            st.markdown(f"Owner: {owner_name} | Available: 8:00 AM - 10:00 PM")
            
            # Display scheduled items
            st.markdown("### Daily Schedule")
            scheduled_items = [item for item in plan if item.scheduled_time >= 0]
            unscheduled_items = [item for item in plan if item.scheduled_time < 0]
            
            if scheduled_items:
                for item in scheduled_items:
                    hours = item.scheduled_time // 60
                    minutes = item.scheduled_time % 60
                    time_str = f"{hours:02d}:{minutes:02d}"
                    st.markdown(
                        f"**{time_str}** - {item.task.title} ({item.duration_minutes}min) "
                        f"[{item.task.priority} priority] — {item.reason}"
                    )
            else:
                st.warning("No tasks could be scheduled within the available time window.")
            
            if unscheduled_items:
                st.markdown("### Could Not Schedule")
                for item in unscheduled_items:
                    st.markdown(f"- {item.task.title} — {item.reason}")
        else:
            st.error("Could not generate a schedule. Check your inputs.")
