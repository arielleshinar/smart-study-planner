import math
class Task:
    # The program models study tasks as objects, sorts them by deadline,
    # and uses a greedy scheduling algorithm to distribute task hours
    # across available days while respecting a daily workload limit.

    def __init__(self, name, deadline, hours, priority=1):
        self.name = name
        self.deadline = deadline
        self.hours = hours
        self.priority = priority

def create_schedule(tasks, max_hours_per_day=4, auto_adjust=False):
    """
    Builds a study schedule and returns:
    - schedule: dict of day -> list of (task_name, hours)
    - messages: list of warnings/info strings
    - adjusted_limit: final max_hours_per_day after any automatic adjustment
    """
    needs_adjustment = False

    if not tasks:
        return {}, [], max_hours_per_day

    tasks.sort(key=lambda t: (t.deadline, -t.priority))
    schedule = {}
    messages = []

    # ---------- feasibility analysis ----------
    max_deadline = max(task.deadline for task in tasks)
    total_required = sum(task.hours for task in tasks)
    total_capacity = max_deadline * max_hours_per_day

    needed_daily_limit = max_hours_per_day
    overload_found = False

    if total_required > total_capacity:
        overload_found = True
        messages.append(
            f"Total workload is {total_required}h, but only {total_capacity}h are available."
        )

    for day in range(1, max_deadline + 1):
        required_by_day = sum(task.hours for task in tasks if task.deadline <= day)
        capacity_by_day = day * max_hours_per_day

        if required_by_day > capacity_by_day:
            overload_found = True
            messages.append(
                f"By day {day}, tasks require {required_by_day}h, but only {capacity_by_day}h are available."
            )
            required_limit_for_day = math.ceil(required_by_day / day)
            needed_daily_limit = max(needed_daily_limit, required_limit_for_day)

    if overload_found and needed_daily_limit > max_hours_per_day:
        needs_adjustment = True
        
        if auto_adjust:
            messages.append(
                f"Daily limit automatically increased from {max_hours_per_day}h to {needed_daily_limit}h."
            )
            max_hours_per_day = needed_daily_limit
        else:
            messages.append(
                f"You need at least {needed_daily_limit}h/day to make the schedule feasible."
            )
            messages.append(
                "Proceeding with the current daily limit. A partial schedule may be created."
            )

    # ---------- actual scheduling ----------
    for task in tasks:
        required_per_day = task.hours / task.deadline
        remaining_hours = task.hours

        if required_per_day > max_hours_per_day:
            messages.append(
                f"'{task.name}' needs about {required_per_day:.1f}h/day to finish by day {task.deadline}, but the current limit is {max_hours_per_day}h/day."
            )

        for day in range(1, task.deadline + 1):
            if remaining_hours == 0:
                break

            if day not in schedule:
                schedule[day] = []

            used_hours = sum(h for _, h in schedule[day])
            available = max_hours_per_day - used_hours

            if available > 0:
                hours_to_assign = min(available, remaining_hours)
                schedule[day].append((task.name, hours_to_assign))
                remaining_hours -= hours_to_assign

        if remaining_hours > 0:
            messages.append(
                f"'{task.name}' could not be fully scheduled. {remaining_hours}h left."
            )

    return schedule, messages, max_hours_per_day, needs_adjustment


def print_schedule(schedule):
    """Takes the schedule dictionary and prints it nicely."""
    for day in sorted(schedule):
        print(f"Day {day}:")
        for task, hours in schedule[day]:
            print(f"  - {task}: {hours}h")


def get_valid_int(prompt, min_value=None, max_value=None):
    """helper function that keeps asking until the user enters a valid integer"""
    while True:
        try:
            value = int(input(prompt))

            if min_value is not None and value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}.")
                continue

            if max_value is not None and value > max_value:
                print(f"Please enter a number less than or equal to {max_value}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    tasks = []

    # ask user for the number of tasks
    n = get_valid_int("Enter number of tasks: ", min_value=0)

    # handle empty case early
    if n == 0:
        print("No tasks entered.")
    else:
        # ask user for task details
        for i in range(n):
            print(f"\nTask {i+1}")

            name = input("Name: ").strip()
            while not name:
                print("Task name cannot be empty.")
                name = input("Name: ").strip()

            deadline = get_valid_int("Deadline (in days): ", min_value=1)
            hours = get_valid_int("Hours needed: ", min_value=1)
            priority = get_valid_int("Priority (1-3): ", min_value=1, max_value=3)

            tasks.append(Task(name, deadline, hours, priority))

        # build and print schedule
        schedule = create_schedule(tasks)
        print_schedule(schedule)