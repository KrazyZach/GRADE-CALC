import tkinter as tk

root = tk.Tk()
root.title("Grade Calculator")
root.geometry("710x600")
root.configure(bg="#f0f8ff")  # Background color for the main window

# Initialize variables
rows = 1
mode = None
gradebook = {"points_earned": 0, "points_total": 0}
entries = []
x = []

# Define styles
style = {
    "font": ("Helvetica", 12),
    "bg": "#f0f8ff",  # Ensure all elements have the same bg color
    "fg": "#333333",
}

button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#4caf50",
    "fg": "#ffffff",
    "relief": "raised",
    "bd": 2,
    "padx": 10,
    "pady": 5,
}

entry_style = {
    "font": ("Helvetica", 12),
    "relief": "solid",
    "bd": 2,
}

label_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#f0f8ff",  # Ensure label backgrounds match the main window
    "fg": "#333333",
}

# Functions
def create():
    global rows
    rows += 1
    if rows <= 0:
        rows = 1
    grade.config(text="")

    # Create assignment labels and entry fields
    assignments = tk.Label(frame, text=f"Assignment {rows}: ", **label_style)
    x.append(assignments)
    assignments.grid(row=rows, column=0, pady=5)

    entry_box_3 = tk.Entry(frame, **entry_style)
    entry_box_4 = tk.Entry(frame, **entry_style)
    entry_box_3.grid(row=rows, column=1, padx=5)
    entry_box_4.grid(row=rows, column=2, padx=5)

    # Add entries to list
    entries.append((entry_box_3, entry_box_4))

    # Update grade label
    grade.grid(row=(rows + 1), column=0, columnspan=3)
    calculate.grid(row=(rows + 2), column=0)
    create_row.grid(row=(rows + 2), column=1)
    delete.grid(row=(rows + 2), column=2)

    # Scroll the canvas down to the newly added row
    canvas.yview_moveto(1)  # Scroll to the bottom (new row)

def check_grade(grade):
    if grade < 60:
        return "F"
    elif grade < 70:
        return "D"
    elif grade < 80:
        return "C"
    elif grade < 90:
        return "B"
    elif grade <= 100:
        return "A"
    else:
        return "This is impossible"

def calc():
    try:
        if mode == "points":
            average = 0
            gradebook["points_earned"] = 0
            gradebook["points_total"] = 0
            for point_earned, point_total in entries:
                if point_earned.get() == "" or point_total.get() == "":
                    continue
                gradebook["points_earned"] += int(point_earned.get())
                gradebook["points_total"] += int(point_total.get())
            average = (gradebook["points_earned"] / gradebook["points_total"]) * 100
        elif mode == "weighted":
            num = 0
            dum = 0
            for grade_prec, weight in entries:
                if grade_prec.get() == "" or weight.get() == "":
                    continue
                x = int(grade_prec.get())
                y = int(weight.get())
                num += float((x * y))
                dum += y
            average = float(num / dum)

        grade.config(text=f"{average:.2f}%, your grade is: {check_grade(average)}")
    
    except UnboundLocalError:
        grade.config(text="Pick a grading style", fg="red")
    except ZeroDivisionError:
        grade.config(text="Error, Division by Zero", fg="red")
    except ValueError:
        grade.config(text="Error, invalid characters", fg="red")
    
    grade.grid(row=(rows + 1), column=0, columnspan=3)

def create_points():
    global mode
    x_axis.config(text="Points earned")
    y_asis.config(text="Points in total")
    mode = "points"

def create_weight():
    global mode
    x_axis.config(text="Grade(%)")
    y_asis.config(text="Weight")
    mode = "weighted"

def resets():
    if rows > 0:
        entry_box_1.delete(0, tk.END)
        entry_box_2.delete(0, tk.END)
        for entry1, entry2 in entries:
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)

def remove():
    global rows
    try:
        if rows > 1:
            entry1, entry2 = entries.pop()
            entry1.destroy()
            entry2.destroy()

            x[-1].destroy()
            x.pop()
            rows -= 1
            grade.grid(row=(rows + 1), column=0, columnspan=3)
            calculate.grid(row=(rows + 2), column=0)
            create_row.grid(row=(rows + 2), column=1)
            delete.grid(row=(rows + 2), column=2)

            # Scroll the canvas up after deleting a row
            canvas.yview_moveto(1)  # Scroll to the bottom

        else:
            grade.config(text="Error, No more rows to delete", fg="red")
            grade.grid(row=8, column=0, columnspan=3)

    except Exception as e:
        grade.config(text=f"Error: {str(e)}", fg="red")

    except UnboundLocalError:
        grade.config(text="Error, No more rows", fg="red")
        grade.grid(row=8, column=0)

# Create main frame and canvas for scrolling
canvas = tk.Canvas(root, bg="#f0f8ff")  # Ensure canvas background matches
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the content
frame = tk.Frame(canvas, bg="#f0f8ff")  # Ensure frame background matches
canvas.create_window((0, 0), window=frame, anchor="nw")

# Bind the scroll region to the frame size with a slight delay to reduce lag
def update_scroll_region():
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", lambda event: root.after(50, update_scroll_region))

# Bind the mouse wheel to scroll the canvas
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

frame.bind_all("<MouseWheel>", on_mouse_wheel)

# Create UI elements inside the frame
assignment = tk.Label(frame, text=f"Assignment {rows}: ", **label_style)
create_row = tk.Button(frame, text="Add Assignment", command=create, **button_style)
calculate = tk.Button(frame, text="Calculate", command=calc, **button_style)
entry_box_1 = tk.Entry(frame, **entry_style)
entry_box_2 = tk.Entry(frame, **entry_style)
entries.append((entry_box_1, entry_box_2))

x_axis = tk.Label(frame, text="", **label_style)
y_asis = tk.Label(frame, text="", **label_style)

modes = tk.Label(frame, text="Choose Grading Mode", **label_style)
weighted_side = tk.Button(frame, text="Weighted Grading", command=create_weight, **button_style)
points_side = tk.Button(frame, text="Points Grading", command=create_points, **button_style)
reset = tk.Button(frame, text="Reset", command=resets, **button_style)
delete = tk.Button(frame, text="Delete row", command=remove, **button_style)

grade = tk.Label(frame, text="", font=("Helvetica", 14, "bold"), bg="#f0f8ff", fg="#4caf50")

# Layout the UI elements inside the frame
assignment.grid(row=1, column=0, pady=5)
entry_box_1.grid(row=1, column=1, padx=5)
entry_box_2.grid(row=1, column=2, padx=5)
calculate.grid(row=2, column=0, padx=10, pady=5)
create_row.grid(row=2, column=1, padx=10, pady=5)
weighted_side.grid(row=0, column=3, padx=10, pady=5)
points_side.grid(row=1, column=3, padx=10, pady=5)
x_axis.grid(row=0, column=1, pady=5)
y_asis.grid(row=0, column=2, pady=5)
reset.grid(row=2, column=3, padx=10, pady=5)
delete.grid(row=2, column=2, padx=10, pady=5)

root.mainloop()
