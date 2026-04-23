import json
import os
from datetime import datetime

# load tasks
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
    return []

# save tasks
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# FORMAT TASK (Procedural abstraction + Urgency system)
def format_task(task):
    today = datetime.today()
    due_date = datetime.strptime(task["date"], "%Y-%m-%d")

    if task["completed"]:
        status = "✔ Completed"
    elif due_date < today:
        status = "❗ Overdue"
    elif (due_date - today).days <= 2:
        status = "⚠ Due Soon"
    else:
        status = "📝 Pending"

    return f"{status} | {task['subject']} | {task['text']} (Due: {task['date']})"

# add task (now includes subject)
def add_task(tasks):
    text = input("Enter assignment: ")
    date = input("Enter due date (YYYY-MM-DD): ")
    subject = input("Enter subject (Math, English, etc.): ")

    if text == "" or date == "" or subject == "":
        print("Fill in all fields!")
        return

    tasks.append({
        "text": text,
        "date": date,
        "subject": subject,
        "completed": False
    })

# view tasks (sorted + iteration)
def view_tasks(tasks):
    tasks.sort(key=lambda x: x["date"])

    if len(tasks) == 0:
        print("No tasks yet!")
        return

    for i in range(len(tasks)):
        print(f"{i + 1}. {format_task(tasks[i])}")

# complete task
def complete_task(tasks):
    view_tasks(tasks)
    choice = int(input("Enter task number to mark complete: ")) - 1

    if 0 <= choice < len(tasks):
        tasks[choice]["completed"] = True

# delete task
def delete_task(tasks):
    view_tasks(tasks)
    choice = int(input("Enter task number to delete: ")) - 1

    if 0 <= choice < len(tasks):
        tasks.pop(choice)

# filter by subject
def filter_by_subject(tasks):
    subject = input("Enter subject to filter: ").lower()

    found = False
    for task in tasks:
        if task["subject"].lower() == subject:
            print(format_task(task))
            found = True

    if not found:
        print("No tasks found for that subject.")

# progress tracker
def show_progress(tasks):
    if len(tasks) == 0:
        print("No tasks to track.")
        return

    completed = sum(1 for task in tasks if task["completed"])
    total = len(tasks)

    percent = (completed / total) * 100

    print(f"Progress: {completed}/{total} tasks completed ({percent:.1f}%)")

# main loop
def main():
    tasks = load_tasks()

    while True:
        print("\n📚 Homework Planner")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Filter by Subject")
        print("6. Show Progress")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            filter_by_subject(tasks)
        elif choice == "6":
            show_progress(tasks)
        elif choice == "7":
            save_tasks(tasks)
            print("Saved. Goodbye!")
            break
        else:
            print("Invalid choice!")

main()