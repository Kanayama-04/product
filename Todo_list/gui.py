import tkinter as tk
import json

def main():
    Width = 300
    Height = 350
    px = 500
    py = 300
    tasks = []
    task_name = []

    with open("tasks.json", "r") as f:
        tasks = json.load(f)

    root = tk.Tk()
    root.geometry(f'{Width}x{Height}+{px}+{py}')

    show_frame = tk.Frame(
        root,
        width=Width,
        height=Height
    )

    show_frame.grid(row=0, column=1)

    tk_task = tk.StringVar(root, value=task_name)

    listbox = tk.Listbox(
        show_frame,
        listvariable=tk_task
    )

    listbox.grid(row=0, column=1, padx=10, pady=10)

    ybar = tk.Scrollbar(
        show_frame,
        orient=tk.VERTICAL,
        repeatdelay=2000,
        repeatinterval=100
    )

    ybar.grid(
        row=0,
        column=2,
        sticky=tk.N+tk.S
    )

    ybar.config(
        command=listbox.yview
    )

    listbox.config(
        yscrollcommand=ybar.set
    )

    task_info(listbox, tasks)

    task = tk.Entry(root, width=12)
    task.grid(row=2, column=2)

    deadline = tk.Entry(root, width=12)
    deadline.grid(row=3, column=2)

    delete_btn = tk.Button(root, text="delete", width=7, command=lambda:delete(task,deadline))
    delete_btn.grid(row=3, column=1)

    add_btn = tk.Button(root, text="add", width=7, command=lambda:get_task(task, deadline, listbox, tasks))
    add_btn.grid(row=2, column=1)

    comp_btn = tk.Button(root, text="complete", width=7, command=lambda:task_is_comp(listbox,tasks))
    comp_btn.grid(row=1, column=1)


    root.mainloop()


def task_info(listbox, tasks):
    for i in range(len(tasks)):
        listbox.insert(tk.END, f'{tasks[i]["task"]} [期日: {tasks[i]["deadline"]}]')

def delete(task, deadline):
    task.detele(0, tk.END)
    deadline.detele(0, tk.END)

def get_task(task, deadline, listbox, tasks):
    listbox.delete(0,tk.END)

    if len(task.get()) != 0 and len(deadline.get()) != 0:
        tasks.append({"task":task.get(), "deadline":deadline.get()})
    
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

    task_info(listbox,tasks)

    delete(task, deadline)


def task_is_comp(listbox, tasks):
    old_tasks = []

    with open("old_task.json", "r") as f:
        old_tasks = json.load(f)
    
    if len(old_tasks) == 10:
        del old_tasks
        old_tasks = []

    selected = listbox.curselection()
    for index in selected[::-1]:
        if len(tasks) != 0:
            listbox.delete(index)

            old_tasks.append(tasks[index])
            with open("old_task.json", "w") as f:
                json.dump(old_tasks, f)

            del tasks[index]

            with open("taks.json", "w") as f:
                json.dump(tasks, f)
            
            listbox.delete(0, tk.END)
            task_info(listbox, tasks)
        else:
            listbox.insert(tk.END, "not fond task")

if __name__ == '__main__':
    main()