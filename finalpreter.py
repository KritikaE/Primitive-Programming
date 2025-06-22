import tkinter as tk
from tkinter import messagebox
import re

#interpreter logic

VAR_NAME_PATTERN = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

def interpret_from_file(file_path, output_widget):
    variables = {}

    with open(file_path, "r") as f:
        program_lines = [line.strip() for line in f.readlines() if line.strip()]

    output_widget.delete("1.0", tk.END)  

    for line in program_lines:
        if line == "STOP":
            break

        if '=' not in line:
            output_widget.insert(tk.END, f"Invalid syntax: {line}\n")
            return

        var, expr = line.split('=', 1)
        var = var.strip()
        expr = expr.strip()

        if not VAR_NAME_PATTERN.fullmatch(var):
            output_widget.insert(tk.END, f"Invalid variable name: {var}\n")
            return

        if not re.fullmatch(r"[A-Za-z0-9_+\-*/(). ]+", expr):
            output_widget.insert(tk.END, f"Invalid characters in expression: {expr}\n")
            return

        try:
            value = eval(expr, {"__builtins__": None}, variables)
        except NameError as e:
            output_widget.insert(tk.END, f"Undefined variable used: {e}\n")
            return
        except Exception as e:
            output_widget.insert(tk.END, f"Error evaluating expression '{expr}': {e}\n")
            return

        if not isinstance(value, (int, float)):
            output_widget.insert(tk.END, "Only numeric results are supported.\n")
            return

        if abs(value) > 999999999:
            output_widget.insert(tk.END, "Value exceeds max allowed digits.\n")
            return

        variables[var] = value

    output_widget.insert(tk.END, "Output from Interpreter:\n")
    for var in sorted(variables.keys()):
        output_widget.insert(tk.END, f"{var} = {variables[var]}\n")

#gui

def save_input_and_run():
    user_input = text_area.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showwarning("Empty", "Please enter some expressions.")
        return

    file_path = "user_program.txt"
    try:
        with open(file_path, "w") as file:
            file.write(user_input)

        messagebox.showinfo("Saved", f"Data saved to {file_path}")
        interpret_from_file(file_path, output_area)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

#user end

root = tk.Tk()
root.title("My Interpreter 😎")
root.geometry("600x600")
root.configure(bg="black")

tk.Label(root, text="Enter expressions (e.g., total = (a + 2) * b - 3).",font=("consolous",16, "bold"),
    bg="black", fg="white"
).pack(pady=(12, 6))

text_area = tk.Text(
    root, height=12, width=70,
    bg="black", fg="white", insertbackground="white", 
    font=("Consolas", 14, "bold")
)
text_area.pack(pady=10)
text_area.focus_set()


run_button = tk.Button(root, text="RUN", command=save_input_and_run)
run_button.pack(pady=10)

tk.Label(root, text="Interpreter Output:", bg='black',fg="white",font=("consolous",16, "bold")).pack()

output_area = tk.Text(root, height=12, width=70, bg='black',fg="white",font=("consolous",14,'bold'))
output_area.pack(pady=10)

root.mainloop()