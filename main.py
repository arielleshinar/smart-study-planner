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


def create_schedule(tasks, max_hours_per_day=4):
    """
    Takes a list of tasks, builds a study schedule, and returns that schedule.

    Parameters:
    - tasks: a list of Task objects
    - max_hours_per_day: default max study time per day is 4 hours
    """

    if not tasks:
        return {}

    # sort tasks by earliest deadline, then by higher priority
    tasks.sort(key=lambda t: (t.deadline, -t.priority))

    # create an empty dictionary to store the final plan
    # each day stores a list of (task_name, hours) pairs
    schedule = {}

    # ---------- global feasibility check ----------
    # Are there enough total hours to finish all tasks?
    max_deadline = max(task.deadline for task in tasks)
    total_capacity = max_deadline * max_hours_per_day
    total_required = sum(task.hours for task in tasks)

    if total_required > total_capacity:
        print(
            f"WARNING: Total workload is {total_required}h, "
            f"but only {total_capacity}h available."
        )

        required_per_day = total_required / max_deadline
        print(
            f"You need about {required_per_day:.1f}h/day "
            f"to complete all tasks."
        )

        choice = input("Would you like to increase the daily limit? (y/n): ")

        if choice.lower() == 'y':
            max_hours_per_day = math.ceil(required_per_day)
            print(f"Updating daily limit to {max_hours_per_day} hours.\n")

    # ---------- actual scheduling ----------
    for task in tasks:
        # calculate required daily hours for this specific task
        required_per_day = task.hours / task.deadline

        # store how many hours are still left to schedule
        remaining_hours = task.hours

        # per-task feasibility check
        if required_per_day > max_hours_per_day:
            print(
                f"WARNING: '{task.name}' needs about {required_per_day:.1f}h/day "
                f"to finish by day {task.deadline}, but the current limit is "
                f"{max_hours_per_day}h/day."
            )

        # go through the allowed days for this task
        for day in range(1, task.deadline + 1):
            if remaining_hours == 0:
                break

            # if this day doesn't exist yet, create it
            if day not in schedule:
                schedule[day] = []

            # calculate how many hours are already used that day
            used_hours = sum(h for _, h in schedule[day])
            available = max_hours_per_day - used_hours

            # only add work if there is room
            if available > 0:
                hours_to_assign = min(available, remaining_hours)
                schedule[day].append((task.name, hours_to_assign))
                remaining_hours -= hours_to_assign

        # warning in case task still could not be fully scheduled
        if remaining_hours > 0:
            print(
                f"WARNING: '{task.name}' could not be fully scheduled. "
                f"{remaining_hours}h left."
            )

    return schedule


def print_schedule(schedule):
    """Takes the schedule dictionary and prints it nicely."""
    for day in sorted(schedule):
        print(f"Day {day}:")
        for task, hours in schedule[day]:
            print(f"  - {task}: {hours}h")


if __name__ == "__main__":
    tasks = []

    # ask user for the number of tasks
    n = int(input("Enter number of tasks: "))

    for i in range(n):
        print(f"\nTask {i+1}")
        name = input("Name: ")
        deadline = int(input("Deadline (in days): "))
        hours = int(input("Hours needed: "))
        priority = int(input("Priority (1-3): "))

        tasks.append(Task(name, deadline, hours, priority))

    schedule = create_schedule(tasks)
    print_schedule(schedule)