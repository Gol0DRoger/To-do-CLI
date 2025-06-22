import sqlite3
from colorama import Fore, Style, init

init(autoreset=True)

# Connect to SQLite
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
)
''')
conn.commit()

def add_task(task):
    cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task,))
    conn.commit()
    print(Fore.GREEN + f"✅ Task added: {task}")

def list_tasks(show_completed=False):
    if show_completed:
        cursor.execute("SELECT * FROM tasks WHERE completed = 1")
    else:
        cursor.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = cursor.fetchall()
    
    if not tasks:
        print(Fore.YELLOW + "📭 No tasks to show.")
        return

    for task in tasks:
        status = Fore.GREEN + "✔ Done" if task[2] else Fore.RED + "❌ Pending"
        print(Fore.CYAN + f"{task[0]}. {task[1]} [{status}]")

def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    if cursor.rowcount:
        conn.commit()
        print(Fore.GREEN + "✅ Task marked as completed.")
    else:
        print(Fore.RED + "⚠️ Task not found.")

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount:
        conn.commit()
        print(Fore.YELLOW + "🗑️ Task deleted.")
    else:
        print(Fore.RED + "⚠️ Task not found.")

def edit_task(task_id, new_text):
    cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_text, task_id))
    if cursor.rowcount:
        conn.commit()
        print(Fore.BLUE + "✏️ Task updated successfully.")
    else:
        print(Fore.RED + "⚠️ Task not found.")

def menu():
    while True:
        print(Style.BRIGHT + "\n" + Fore.MAGENTA + "--- TO-DO LIST MENU ---")
        print("1. Add Task")
        print("2. View Pending Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. View Completed Tasks")
        print("6. Edit a Task")
        print("7. Exit")

        choice = input(Fore.WHITE + "Choose an option: ")

        if choice == '1':
            task = input("Enter task: ")
            add_task(task)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = input("Enter task ID to complete: ")
            complete_task(int(task_id))
        elif choice == '4':
            task_id = input("Enter task ID to delete: ")
            delete_task(int(task_id))
        elif choice == '5':
            list_tasks(show_completed=True)
        elif choice == '6':
            task_id = input("Enter task ID to edit: ")
            new_text = input("Enter new task text: ")
            edit_task(int(task_id), new_text)
        elif choice == '7':
            print(Fore.CYAN + "👋 Goodbye!")
            break
        else:
            print(Fore.RED + "❗Invalid choice, try again.")

if __name__ == "__main__":
    menu()
    conn.close()
