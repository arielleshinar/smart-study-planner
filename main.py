class Task:
#The program models study tasks as objects, sorts them by deadline, 
#and uses a greedy scheduling algorithm to distribute task hours 
#across available days while respecting a daily workload limit.
#detects infeasible schedules


#the class represents one study task, e.g Math HW, CS Project..
#each task has a few pieces of information: its name, deadline and how long it takes
    def __init__(self, name, deadline, hours, priority=1):
        self.name = name
        self.deadline = deadline
        self.hours = hours
        self.priority = priority

def create_schedule(tasks, max_hours_per_day=4):
    """"takes a list of tasks, builds a study schedule and returns that schedule
    parameters: tasks - a list of Task objects, max_hours_per_day=4 - default max studytime per day is 4 hours"""
    
    # sort tasks by earliest deadline (t.deadline) if deadlines are equal then by priority (negative so descending)
    tasks.sort(key=lambda t: (t.deadline, -t.priority))
    #create an empty dictionary (schedule) to store the final plan 
    #each day stores a list of (task_name, hours) pairs
    schedule = {}

    #goes through the sorted list one task at a time
    for task in tasks:
        #at the start of each stack we store how many hours are still left to schedule
        #as we place hours into days, we reduce this number
        remaining_hours = task.hours

        #goes through the allowed days for this task
        for day in range(1, task.deadline + 1):
            if remaining_hours == 0:
                #if we already assigned the task fully stops loop
                break
            
            #if this day doesn't exist yet in the dictionary, create it with an empty list so we can add tasks to it
            if day not in schedule:
                schedule[day] = []

            #checks how many hours of a certain day are already used
            used_hours = sum(h for _, h in schedule[day])
            available = max_hours_per_day - used_hours

            #only add work if there is room
            if available > 0:
                #we assign the min of how much room is left today and how many task hours are sill needed
                hours_to_assign = min(available, remaining_hours)
                #add the task to the schedual (adding the task and the hours to assign to that days list)
                schedule[day].append((task.name, hours_to_assign))
                #subtracting the hours we just schedualed
                remaining_hours -= hours_to_assign
    
    #warning in case of impossible schedule (will still build partial schedule)
    if remaining_hours > 0:
        print(f"WARNING: '{task.name}' could not be fully scheduled. {remaining_hours}h left.")

    return schedule


def print_schedule(schedule):
    """takes the schedule dictionary and prints it nicely"""
    #get the dictionary keys (the day numbers) in sorted order
    for day in sorted(schedule):
        print(f"Day {day}:")
        for task, hours in schedule[day]:
            print(f"  - {task}: {hours}h")

#only run the code below if this file is being run directly
if __name__ == "__main__":
    #creates a list of Task objects
    #tasks = [
    #    Task("Math HW", 2, 3), #creates task with name=Math HW, deadline=2 days, takes=3 hours
    #    Task("CS Project", 3, 5),
    #    Task("Exam Study", 1, 4)
    #]
    
    #tasks = [
    #   Task("Big Project", 2, 10),
    #   Task("Small Task", 1, 2)
    #]

    tasks = [
        Task("Math HW", 2, 3, priority=1),
        Task("Physics Review", 2, 2, priority=3),
        Task("CS Project", 3, 5, priority=2)
    ]

    #builds the schedule and prints it
    schedule = create_schedule(tasks)
    print_schedule(schedule)