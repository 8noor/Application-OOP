import json
from datetime import datetime

class Task:
    def __init__(self, title, priority="Medium", due_date=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        task = Task(data["title"], data["priority"], data["due_date"])
        task.completed = data["completed"]
        return task

    def __str__(self):
        status = "✅" if self.completed else "❌"
        return f"[{status}] {self.title} | Priority: {self.priority} | Due: {self.due_date or 'N/A'}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def list_tasks(self, show_completed=None):
        for i, task in enumerate(self.tasks):
            if show_completed is None or task.completed == show_completed:
                print(f"{i + 1}. {task}")

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def save_to_file(self, filename="tasks.json"):
        with open(filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_from_file(self, filename="tasks.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []


class TaskApp:
    def __init__(self):
        self.manager = TaskManager()
        self.manager.load_from_file()

    def run(self):
        print("📋 Welcome to the OOP Task Manager CLI")
        while True:
            print("\n1. Add Task\n2. List Tasks\n3. Complete Task\n4. Save\n5. Quit")
            choice = input("Choose an option: ")

            if choice == "1":
                title = input("Task title: ")
                priority = input("Priority (Low/Medium/High): ")
                due_date = input("Due date (YYYY-MM-DD or leave blank): ")
                task = Task(title, priority, due_date or None)
                self.manager.add_task(task)

            elif choice == "2":
                print("\n--- All Tasks ---")
                self.manager.list_tasks()

            elif choice == "3":
                self.manager.list_tasks(show_completed=False)
                index = int(input("Enter task number to complete: ")) - 1
                self.manager.complete_task(index)

            elif choice == "4":
                self.manager.save_to_file()
                print("✅ Tasks saved.")

            elif choice == "5":
                self.manager.save_to_file()
                print("👋 Bye!")
                break
            else:
                print("Invalid choice. Try again.")

# Run the app
if __name__ == "__main__":
    app = TaskApp()
    app.run()
