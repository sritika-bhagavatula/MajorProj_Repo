# task.py
class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

import tkinter as tk
from tkinter import messagebox
import json

# Import Task class (from task.py if in a separate file)
class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        return f"{self.title} - {self.category} - {'Completed' if self.completed else 'Pending'}"

# File handling for loading and saving tasks
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

# Main Tkinter Application
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = load_tasks()

        # UI Elements
        self.title_label = tk.Label(root, text="Task Title:")
        self.title_label.grid(row=0, column=0)

        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.grid(row=0, column=1)

        self.desc_label = tk.Label(root, text="Task Description:")
        self.desc_label.grid(row=1, column=0)

        self.desc_entry = tk.Entry(root, width=40)
        self.desc_entry.grid(row=1, column=1)

        self.cat_label = tk.Label(root, text="Category (Work, Personal, Urgent):")
        self.cat_label.grid(row=2, column=0)

        self.cat_entry = tk.Entry(root, width=40)
        self.cat_entry.grid(row=2, column=1)

        # Add Task Button
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=1, sticky='e')

        # Listbox for viewing tasks
        self.task_listbox = tk.Listbox(root, height=10, width=60)
        self.task_listbox.grid(row=4, column=0, columnspan=2)

        # Buttons for task management
        self.complete_button = tk.Button(root, text="Mark Completed", command=self.mark_task_completed)
        self.complete_button.grid(row=5, column=0, sticky='w')

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=5, column=1, sticky='e')

        self.load_tasks_in_listbox()

    def load_tasks_in_listbox(self):
        """Load tasks from the task list into the listbox."""
        self.task_listbox.delete(0, tk.END)  # Clear the listbox first
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        """Add a new task."""
        title = self.title_entry.get()
        description = self.desc_entry.get()
        category = self.cat_entry.get()

        if not title or not description or not category:
            messagebox.showwarning("Input Error", "Please provide all task details.")
            return

        new_task = Task(title, description, category)
        self.tasks.append(new_task)
        self.load_tasks_in_listbox()

        # Clear the entries
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.cat_entry.delete(0, tk.END)

    def mark_task_completed(self):
        """Mark the selected task as completed."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            selected_task = self.tasks[selected_index]
            selected_task.mark_completed()
            self.load_tasks_in_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        """Delete the selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_index)
            self.load_tasks_in_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def on_closing(self):
        """Save tasks when closing the application."""
        save_tasks(self.tasks)
        self.root.destroy()

# Main function to start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Save tasks on window close
    root.mainloop()
