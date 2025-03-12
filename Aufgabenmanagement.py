import customtkinter as ctk
from tkinter import ttk
from datetime import date

def on_button_click():
    global issue_var
    global due_var
    global even
    global today
    task = taskEntry.get()
    description = descriptionEntry.get()
    issueDate = Issue_DateEntry.get()
    dueDate = Due_DateEntry.get()
    priority = PrioritySelect.get()
    if task:
        if even:
            tree.insert("", "end", values=(task,description, issueDate, dueDate, priority), tags=("even",))
            tree.tag_configure("even", background="#f0f0f0")
            even = not even
        else:
            tree.insert("", "end", values=(task,description, issueDate, dueDate, priority), tags=("odd",))
            tree.tag_configure("odd", background="#e0e0e0")
            even = not even
        taskEntry.delete(0, ctk.END)
        descriptionEntry.delete(0, ctk.END)
        issue_var.set(today)
        due_var.set(today)
        # PriorityEntry.delete(0, ctk.END)

def remove_selected():
    selected_item = tree.selection()
    for item in selected_item:
        tree.delete(item)

even = False

# Create main window
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Simple GUI")
root.geometry("1000x500")

columns = ("Task", "Description", "Issue_Date", "Due_Date", "Priority")
priorities = ["Low", "Standard", "High", "Critical"]

input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=10)

# Create widgets
# for i in range(0, len(columns)):
#     exec(f'{columns[i]}Label = ctk.CTkLabel(root, text="{columns[i]}")')
#     exec(f'{columns[i]}Label.grid(row=0, column={i}, padx=5)')
#     exec(f'{columns[i]}Label.pack(pady=10)')
#     exec(f'{columns[i]}Entry = ctk.CTkEntry(root)')
#     # exec(f'{columns[i]}Entry.pack(pady=5)')

taskLabel = ctk.CTkLabel(input_frame, text="Task")
taskLabel.grid(row=0, column=0, padx=5)
taskEntry = ctk.CTkEntry(input_frame)
taskEntry.grid(row=1, column=0, padx=5, pady=5)

descriptionLabel = ctk.CTkLabel(input_frame, text="Description")
descriptionLabel.grid(row=0, column=1, padx=5)
descriptionEntry = ctk.CTkEntry(input_frame)
descriptionEntry.grid(row=1, column=1, padx=5, pady=5)

today = date.today().strftime("%d.%m.%Y")
issue_var = ctk.StringVar()
issue_var.set(today)
due_var = ctk.StringVar()
due_var.set(today)

Issue_DateLabel = ctk.CTkLabel(input_frame, text="Issue_Date")
Issue_DateLabel.grid(row=0, column=3, padx=5)
Issue_DateEntry = ctk.CTkEntry(input_frame, textvariable=issue_var)
Issue_DateEntry.grid(row=1, column=3, padx=5, pady=5)

Due_DateLabel = ctk.CTkLabel(input_frame, text="Due_Date")
Due_DateLabel.grid(row=0, column=4, padx=5)
Due_DateEntry = ctk.CTkEntry(input_frame, textvariable=due_var)
Due_DateEntry.grid(row=1, column=4, padx=5, pady=5)

PriorityLabel = ctk.CTkLabel(input_frame, text="Priority")
PriorityLabel.grid(row=0, column=5, padx=5)
PrioritySelect = ctk.CTkOptionMenu(input_frame, values=priorities)
PrioritySelect.grid(row=1, column=5, padx=5, pady=5)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

button = ctk.CTkButton(button_frame, text="Add", command=lambda: on_button_click())
button.grid(row=2, column=0, padx=5, pady=5)

remove_button = ctk.CTkButton(button_frame, text="Remove Selected", command=remove_selected)
remove_button.grid(row=2, column=1, padx=5, pady=5)

# Create table (treeview) inside a frame
table_frame = ctk.CTkFrame(root)
table_frame.pack(pady=10, fill=ctk.BOTH, expand=True)

style = ttk.Style(table_frame)
style.configure("Treeview", foreground="white") #sets background and text colors. #343638
style.configure("Treeview.Heading", background="#2b2b2b", foreground="white") #sets heading background and text colors.

tree = ttk.Treeview(table_frame, columns=columns, show="headings")

table_frame.configure(fg_color="#343638")

for column in columns:
    tree.heading(column, text=column)

# tree.heading("Task", text="Task")
# tree.heading("Description", text="Description")
# # tree.heading("Issue Date", text="Issue Date")
# # tree.heading("Due Date", text="Due Date")
# tree.heading("Priority", text="Priority")

tree.pack(pady=10, fill=ctk.BOTH, expand=True)

# Run the GUI event loop
root.mainloop()