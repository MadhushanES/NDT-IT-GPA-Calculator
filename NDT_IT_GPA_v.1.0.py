import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

class GPACalculator:
    def __init__(self, grade_points_csv):
        self.grade_points = pd.read_csv(grade_points_csv).set_index("grade").to_dict()["points"]
        self.semester_data = {}  # Store selected modules for each semester

    def load_modules(self, semester_csv):
        return pd.read_csv(semester_csv).set_index("module").to_dict()["credits"]

    def add_module_grade(self, semester, module, grade):
        credits = self.semester_data[semester]["modules"][module]
        points = self.grade_points[grade]
        self.semester_data[semester]["selected_modules"].append((module, credits, points))

    def calculate_gpa(self, selected_modules):
        total_points = sum(credits * points for _, credits, points in selected_modules)
        total_credits = sum(credits for _, credits, _ in selected_modules)
        return total_points / total_credits if total_credits else 0

    def calculate_overall_gpa(self):
        all_modules = [module for data in self.semester_data.values() for module in data["selected_modules"]]
        return self.calculate_gpa(all_modules)

    def classify_gpa(self, gpa):
        if gpa >= 3.7:
            return "Distinction"
        elif gpa >= 3.0:
            return "Merit Pass"
        elif gpa >= 2.0:
            return "Pass"
        else:
            return "Fail"

# GUI
root = tk.Tk()
root.title("NDT IT GPA Calculator by __mesp__")
root.geometry("600x600")
root.resizable(False, False)  # Disable window resizing
root.attributes("-toolwindow", 1)  # Disable maximize button on some platforms

style = ttk.Style()
style.configure("TNotebook.Tab", padding=[20, 15], font=('Arial', 12, 'bold'))
style.configure("TFrame", background="lightblue")

grade_points_csv = "grade_points.csv"
gpa_calculator = GPACalculator(grade_points_csv)

# Add Notebook for semesters
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Function to update each semester tab
def update_semester_tab(semester, modules_csv):
    gpa_calculator.semester_data[semester] = {
        "modules": gpa_calculator.load_modules(modules_csv),
        "selected_modules": []
    }
    semester_frame = ttk.Frame(notebook)
    notebook.add(semester_frame, text=f"Semester {semester}")

    module_var = tk.StringVar(root)
    grade_var = tk.StringVar(root)
    
    # Adjusted widths for module and grade dropdowns
    module_dropdown = ttk.Combobox(semester_frame, textvariable=module_var, values=list(gpa_calculator.semester_data[semester]["modules"].keys()), width=50)  # Increased width for module dropdown
    module_dropdown.grid(row=0, column=0, padx=10, pady=10)
    
    grade_dropdown = ttk.Combobox(semester_frame, textvariable=grade_var, values=list(gpa_calculator.grade_points.keys()), width=5)  # Reduced width for grade dropdown
    grade_dropdown.grid(row=0, column=1, padx=10, pady=10)
    
    def add_module_to_semester():
        module = module_var.get()
        grade = grade_var.get()
        # Check if the module has already been added
        if any(module == mod for mod, _, _ in gpa_calculator.semester_data[semester]["selected_modules"]):
            # Show a message to the user
            messagebox.showinfo("Duplicate Module", f"The module '{module}' has already been added to Semester {semester}.")
            return
        
        if module and grade:  # Ensure both module and grade are selected
            gpa_calculator.add_module_grade(semester, module, grade)
            module_listbox.insert(tk.END, f"{module} - {grade}")
            
            # Reset dropdowns after adding the module
            module_var.set('')  # Clears the module dropdown selection
            grade_var.set('')   # Clears the grade dropdown selection

    add_button = ttk.Button(semester_frame, text="Add Module", command=add_module_to_semester)
    add_button.grid(row=0, column=2, padx=10, pady=10)
    
    module_listbox = tk.Listbox(semester_frame, height=10, width=60)
    module_listbox.grid(row=1, column=0, columnspan=3, pady=10)
    
    # Semester GPA box
    semester_gpa_output = tk.Text(semester_frame, height=2, width=30, font=("Arial", 12), wrap="word", bg="lightcyan")
    semester_gpa_output.grid(row=3, column=0, columnspan=3, pady=10)
    semester_gpa_output.config(state="disabled")  # Make GPA output read-only

    def calculate_semester_gpa():
        semester_gpa = gpa_calculator.calculate_gpa(gpa_calculator.semester_data[semester]["selected_modules"])
        semester_gpa_output.config(state="normal")
        semester_gpa_output.delete("1.0", tk.END)
        semester_gpa_output.insert(tk.END, f"Semester {semester} GPA: {semester_gpa:.2f}")
        semester_gpa_output.config(state="disabled")

    calculate_button = ttk.Button(semester_frame, text="Calculate Semester GPA", command=calculate_semester_gpa)
    calculate_button.grid(row=2, column=0, columnspan=3, pady=10)

# Load semester data
update_semester_tab(1, "semester1.csv")
update_semester_tab(2, "semester2.csv")
update_semester_tab(3, "semester3.csv")
update_semester_tab(4, "semester4.csv")

# Overall GPA and classification display
def calculate_overall_gpa():
    overall_gpa = gpa_calculator.calculate_overall_gpa()
    classification = gpa_calculator.classify_gpa(overall_gpa)
    overall_gpa_output.config(state="normal")  # Enable editing temporarily to update text
    overall_gpa_output.delete("1.0", tk.END)
    overall_gpa_output.insert(tk.END, f"Overall GPA: {overall_gpa:.2f}\nClassification: {classification}")
    overall_gpa_output.config(state="disabled")  # Disable editing again

overall_button = ttk.Button(root, text="Calculate Overall GPA", command=calculate_overall_gpa)
overall_button.pack(pady=10)

# Text box to display the overall GPA and classification (non-editable)
overall_gpa_output = tk.Text(root, height=3, width=30, font=("Arial", 12), wrap="word", bg="lightyellow")
overall_gpa_output.pack(pady=10)
overall_gpa_output.config(state="disabled")  # Make text box read-only

root.mainloop()
