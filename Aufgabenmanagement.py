import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from datetime import date
import os.path
import csv

def on_button_click():
    global issue_var
    global due_var
    global priority_var
    global even
    global today
    task = taskEntry.get()
    description = descriptionEntry.get()
    issueDate = Issue_DateEntry.get()
    dueDate = Due_DateEntry.get()
    priority = PrioritySelect.get()
    if task:
        insert_row(task, description, issueDate, dueDate, priority, even, True)
        taskEntry.delete(0, ctk.END)
        descriptionEntry.delete(0, ctk.END)
        issue_var.set(today)
        due_var.set(today)
        priority_var.set(priorities[1])

def insert_row(task, description, issueDate, dueDate, priority, even, wr_file):
    if task:
        if even:
            tree.insert("", "end", values=(task,description, issueDate, dueDate, priority), tags=("even",))
            tree.tag_configure("even", background="#242424", foreground="white")
            even = not even
        else:
            tree.insert("", "end", values=(task,description, issueDate, dueDate, priority), tags=("odd",))
            tree.tag_configure("odd", background="#343638", foreground="white")
            even = not even
        if wr_file:
            write_file()

def write_file():
    with open("./tasks.csv", "w") as file:
        # Writing header to csv file
        file.write(columns_string + "\n")

        # Writing all current tree rows to csv
        for item_id in tree.get_children():
            values = tree.item(item_id, 'values')
            csv_string = ",".join(str(item) for item in values)
            file.write(csv_string + "\n")
        file.close()

def remove_selected():
    selected_item = tree.selection()
    for item in selected_item:
        tree.delete(item)
    write_file()

def edit_column(row_id, column_index, new_value):
    """Edits a specific column in a Treeview row."""
    current_values = list(tree.item(row_id, 'values'))  # Get current values as a list
    current_values[column_index] = new_value  # Modify the specific column
    tree.item(row_id, values=current_values)  # Update the row

def handle_double_click(event):
    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if row_id and column_id:
        column_index = int(column_id[1:]) - 1
        current_values = list(tree.item(row_id, 'values'))
        current_value = current_values[column_index]

        new_value = tk.simpledialog.askstring("Edit Field", "Enter new value:", initialvalue=current_value)

        current_values[column_index] = new_value
        tree.item(row_id, values=current_values)

even = False

# Defining table columns
columns = ("Task", "Description", "Issue_Date", "Due_Date", "Priority")

# Initializing string to be written to csv
columns_string = ""
for column in columns:
    columns_string = columns_string + column + ","
columns_string = columns_string[:-1]

# Check if tasks file already exists
file_path = "./tasks.csv"

# Create main window
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Simple GUI")
root.geometry("1000x500")

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
priority_var = ctk.StringVar()
priority_var.set(priorities[1])
PrioritySelect = ctk.CTkOptionMenu(input_frame, values=priorities, variable=priority_var)
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
style.theme_use("clam")
style.configure("Treeview", foreground="black", fieldbackground="#242424") #sets text colors #343638
style.configure("Treeview.Heading", background="#2b2b2b", foreground="white") #sets heading background and text colors.

tree = ttk.Treeview(table_frame, columns=columns, show="headings")

table_frame.configure(fg_color="#343638")

for column in columns:
    tree.heading(column, text=column)

# Preventing all but the description column from stretching
for i in range(0, len(columns)):
    if i != 1:
        tree.column(columns[i], stretch=tk.NO)
    else:
        tree.column(columns[i], stretch=tk.YES)


# tree.heading("Task", text="Task")
# tree.heading("Description", text="Description")
# # tree.heading("Issue Date", text="Issue Date")
# # tree.heading("Due Date", text="Due Date")
# tree.heading("Priority", text="Priority")

tree.pack(pady=10, fill=ctk.BOTH, expand=True)

tree.bind("<Double-1>", handle_double_click)

if os.path.exists(file_path):
    print("File exists. Reading entries...")
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(row)
            task, description, issueDate, dueDate, priority = row
            # Inserting row into tree without writing it to file again
            insert_row(task, description, issueDate, dueDate, priority, even, wr_file=False)                     
else:
    print(f"The file '{file_path}' does not exist. Creating file...")
    try:
        with open("./tasks.csv", "w") as file:
            file.write(columns_string)
            file.close()
        print("File created successfully.")
    except Exception as e:
        print(f"An error occured: {e}")

# Run the GUI event loop
root.mainloop()