import tkinter as tk
from tkinter import messagebox, scrolledtext
from clips import Environment
from datetime import datetime
from collections import Counter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# CLIPS ENVIRONMENT
env = Environment()

env.build("""
(deftemplate symptom (slot code))
""")

env.build("""
(deftemplate diagnosis (slot result))
""")

# RULES (VALIDATED RULES)
# ------------------------------Mild---------------------------------------------
# Rule 1
# IF G001: Memory decline 
# AND G002: Looks confused in familiar places
# THEN G003: Requires a long time to make decisions 
env.build("""
(defrule rule1
   (symptom (code G001))
   (symptom (code G002))
   =>
   (assert (symptom (code G003)))
)
""")

# Rule 2
# IF G003: Requires a long time to make decisions 
# AND G004: Daily activities slower than usual 
# AND G005: Loss of initiative
# THEN G006: Personality changes begin to appear 
env.build("""
(defrule rule2
   (symptom (code G003))
   (symptom (code G004))
   (symptom (code G005))
   =>
   (assert (symptom (code G006)))
)
""")

# Rule 3
# IF G006: Personality changes begin to appear
# THEN P001: Alzheimer’s Dementia (Mild)
env.build("""
(defrule rule3
   (symptom (code G006))
   =>
   (assert (diagnosis (result P001)))
)
""")

# ------------------------------Moderate---------------------------------------------
# Rule 4
# IF G007: Memory is getting worse
# AND G008: Difficulty thinking logically
# AND G009: Difficulty reading, writing, counting
# THEN G010: Easily forgets family members
env.build("""
(defrule rule4
   (symptom (code G007))
   (symptom (code G008))
   (symptom (code G009))
   =>
   (assert (symptom (code G010)))
)
""")

# Rule 5
# IF G011: Cannot learn new things 
# AND G012: Restless, anxious, sad (especially at night)
# THEN G013: Repeats the same conversation 
env.build("""
(defrule rule5
   (symptom (code G011))
   (symptom (code G012))
   =>
   (assert (symptom (code G013)))
)
""")

# Rule 6
# IF G014: Repeats the same movements 
# AND G015: Difficulty controlling emotions and behavior
# THEN G016: Hallucinations (CF = 0.60)
env.build("""
(defrule rule6
   (symptom (code G014))
   (symptom (code G015))
   =>
   (assert (symptom (code G016)))
)
""")

# Rule 7
# IF G010: Forgets family members
# AND G013: Repetitive speech
# AND G016: Hallucinations
# THEN P002: Alzheimer’s Ataxia (Moderate)
env.build("""
(defrule rule7
   (symptom (code G010))
   (symptom (code G013))
   (symptom (code G016))
   =>
   (assert (diagnosis (result P002)))
)
""")

# ------------------------------Acute---------------------------------------------
# Rule 8
# IF G017: Convulsions
# AND G018: Difficulty swallowing food
# THEN G019: Depression and weight loss
env.build("""
(defrule rule8
   (symptom (code G017))
   (symptom (code G018))
   =>
   (assert (symptom (code G019)))
)
""")

# Rule 9
# IF G019: Depression and weight loss
# AND G020: Cannot communicate properly
# AND G021: Cannot recognize close family members
# THEN P003: Acute Alzheimer’s 
env.build("""
(defrule rule9
   (symptom (code G019))
   (symptom (code G020))
   (symptom (code G021))
   =>
   (assert (diagnosis (result P003)))
)
""")

# main Window
root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("900x700")
root.configure(bg="#F4F6F8")

# functions
def save_diagnosis_to_file(selected_symptoms, diagnosis_result):
    with open("diagnosis_records.txt", "a", encoding="utf-8") as file:
        file.write("----------------------------------------\n")
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Selected Symptoms: {', '.join(selected_symptoms)}\n")
        file.write(f"Diagnosis Result: {diagnosis_result}\n")

def diagnose():
    env.reset()
    selected_symptoms = []

    for code, var in symptom_vars.items():
        if var.get():
            env.assert_string(f"(symptom (code {code}))")
            selected_symptoms.append(code)

    env.run()

    diagnoses = [fact["result"] for fact in env.facts() if fact.template.name == "diagnosis"]

    if "P003" in diagnoses:
        result_code = "P003"
        msg = "Diagnosis: Acute Alzheimer’s (P003)"
    elif "P002" in diagnoses:
        result_code = "P002"
        msg = "Diagnosis: Moderate Alzheimer’s (P002)"
    elif "P001" in diagnoses:
        result_code = "P001"
        msg = "Diagnosis: Mild Alzheimer’s (P001)"
    else:
        result_code = "None"
        msg = "No Alzheimer’s stage detected."

    save_diagnosis_to_file(selected_symptoms, result_code)

    messagebox.showinfo(
        "Diagnosis Result",
        msg + "\n\n⚠️ This is a preliminary screening.\nConsult medical professionals."
    )

def show_pie_chart_page():
    admin_records_page.pack_forget()
    pie_chart_page.pack(fill="both", expand=True)

    for widget in pie_chart_frame.winfo_children():
        widget.destroy()

    try:
        with open("diagnosis_records.txt", "r", encoding="utf-8") as f:
            results = [line.split(":")[-1].strip() for line in f if line.startswith("Diagnosis Result:")]
    except FileNotFoundError:
        messagebox.showwarning("No Data", "No records found.")
        return

    if not results:
        messagebox.showwarning("No Data", "No diagnosis data available.")
        return

    count = Counter(results)
    labels, sizes = [], []

    mapping = {
        "P001": "Mild Alzheimer’s",
        "P002": "Moderate Alzheimer’s",
        "P003": "Acute Alzheimer’s",
        "None": "No Alzheimer’s"
    }

    for k, v in count.items():
        labels.append(f"{mapping[k]} ({k})")
        sizes.append(v)

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    ax.set_title("Diagnosis Distribution")

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# start page
start_page = tk.Frame(root, bg="#F4F6F8")
start_page.pack(fill="both", expand=True)

tk.Label(start_page, text="🧠 Alzheimer’s Disease Screening Expert System",
         font=("Segoe UI", 22, "bold"), bg="#F4F6F8").pack(pady=60)

tk.Button(start_page, text="▶ Start Testing", font=("Segoe UI", 16, "bold"),
          bg="#28B463", fg="white", padx=40, pady=15,
          command=lambda: (start_page.pack_forget(), diagnosis_page.pack(fill="both", expand=True))).pack(pady=20)

tk.Button(start_page, text="Admin Login", font=("Segoe UI", 10),
          bg="#D5DBDB", fg="black", padx=15, pady=5,
          command=lambda: (start_page.pack_forget(), admin_login_page.pack(fill="both", expand=True))).pack(pady=10)

tk.Label(start_page, text="Educational use only | Rule-Based Expert System | TES6313",
         font=("Segoe UI", 10), fg="gray", bg="#F4F6F8").pack(side="bottom", pady=15)

# diagnosis page
diagnosis_page = tk.Frame(root, bg="#F4F6F8")
header = tk.Frame(diagnosis_page, bg="#2E86C1", height=80)
header.pack(fill="x")

tk.Label(header, text="Select Patient Symptoms", font=("Segoe UI", 18, "bold"),
         bg="#2E86C1", fg="white").pack(pady=20)

card = tk.Frame(diagnosis_page, bg="white")
card.pack(padx=40, pady=20, fill="both", expand=True)

canvas = tk.Canvas(card, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
symptom_frame = tk.Frame(canvas, bg="white")

canvas.create_window((0, 0), window=symptom_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
scrollbar.pack(side="right", fill="y", padx=(0, 20))
symptom_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

symptoms = {
    "G001": "Memory decline",
    "G002": "Confused in familiar places",
    "G004": "Daily activities slower than usual",
    "G005": "Loss of initiative",
    "G007": "Memory getting worse",
    "G008": "Difficulty thinking logically",
    "G009": "Difficulty reading / writing / counting",
    "G011": "Cannot learn new things",
    "G012": "Restless or anxious at night",
    "G014": "Repeats same movements",
    "G015": "Difficulty controlling emotions",
    "G017": "Convulsions",
    "G018": "Difficulty swallowing food",
    "G020": "Cannot communicate properly",
    "G021": "Cannot recognize close family members"
}

symptom_vars = {}
for code, text in symptoms.items():
    symptom_vars[code] = tk.BooleanVar()
    tk.Checkbutton(symptom_frame, text=text, variable=symptom_vars[code],
                   bg="white", font=("Segoe UI", 12), anchor="w", padx=20).pack(fill="x", pady=4)

button_frame = tk.Frame(diagnosis_page, bg="#F4F6F8")
button_frame.pack(pady=20)

tk.Button(button_frame, text="⬅ Back", font=("Segoe UI", 14, "bold"),
          bg="#D5DBDB", fg="black", padx=20, pady=10,
          command=lambda: (diagnosis_page.pack_forget(), start_page.pack(fill="both", expand=True))).pack(side="left", padx=10)

tk.Button(button_frame, text="🔍 Run Diagnosis", font=("Segoe UI", 14, "bold"),
          bg="#28B463", fg="white", padx=20, pady=10, command=diagnose).pack(side="left", padx=10)

# admin login page
admin_login_page = tk.Frame(root, bg="#F4F6F8")

tk.Label(admin_login_page, text="Admin Login", font=("Segoe UI", 18, "bold"), bg="#F4F6F8").pack(pady=40)
tk.Label(admin_login_page, text="Email:", font=("Segoe UI", 12), bg="#F4F6F8").pack(pady=5)
admin_email_entry = tk.Entry(admin_login_page, font=("Segoe UI", 12))
admin_email_entry.pack(pady=5)

tk.Label(admin_login_page, text="Password:", font=("Segoe UI", 12), bg="#F4F6F8").pack(pady=5)
admin_password_entry = tk.Entry(admin_login_page, font=("Segoe UI", 12), show="*")
admin_password_entry.pack(pady=5)

def admin_login_check():
    email = admin_email_entry.get().strip()
    password = admin_password_entry.get().strip()

    try:
        with open("admin.txt", "r", encoding="utf-8") as f:
            admins = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", "Admin file not found.")
        return

    for admin_email, admin_pass in admins:
        if email == admin_email and password == admin_pass:
            messagebox.showinfo("Success", "Login successful!")
            admin_login_page.pack_forget()
            admin_records_page.pack(fill="both", expand=True)
            load_admin_records() 
            return

    messagebox.showerror("Failed", "Invalid email or password.")

button_frame_admin = tk.Frame(admin_login_page, bg="#F4F6F8")
button_frame_admin.pack(pady=20)

tk.Button(button_frame_admin, text="⬅ Back", font=("Segoe UI", 12, "bold"),
          bg="#D5DBDB", fg="black", padx=15, pady=5,
          command=lambda: (admin_login_page.pack_forget(), start_page.pack(fill="both", expand=True))).pack(side="left", padx=10)

tk.Button(button_frame_admin, text="Login", font=("Segoe UI", 12, "bold"),
          bg="#28B463", fg="white", padx=15, pady=5, command=admin_login_check).pack(side="left", padx=10)

# admin view records page
admin_records_page = tk.Frame(root, bg="#F4F6F8")
tk.Label(admin_records_page, text="Admin Records", font=("Segoe UI", 18, "bold")).pack(pady=10)

admin_text = scrolledtext.ScrolledText(admin_records_page, width=80, height=20)
admin_text.pack(padx=10, pady=10)

def load_admin_records():
    admin_text.delete("1.0", tk.END)
    try:
        with open("diagnosis_records.txt", "r", encoding="utf-8") as f:
            admin_text.insert(tk.END, f.read())
    except FileNotFoundError:
        admin_text.insert(tk.END, "No records found.")

tk.Button(admin_records_page, text="📊 View Pie Chart", font=("Segoe UI", 12, "bold"),
          bg="#5DADE2", fg="white", command=show_pie_chart_page).pack(pady=10)

tk.Button(admin_records_page, text="⬅ Back", font=("Segoe UI", 12, "bold"),
          bg="#D5DBDB", fg="black", command=lambda: (admin_records_page.pack_forget(), start_page.pack(fill="both", expand=True))).pack()

# pie chart page
pie_chart_page = tk.Frame(root, bg="#F4F6F8")
pie_chart_frame = tk.Frame(pie_chart_page, bg="#F4F6F8")
pie_chart_frame.pack(fill="both", expand=True)

tk.Button(pie_chart_page, text="⬅ Back", font=("Segoe UI", 12, "bold"),
          bg="#D5DBDB", fg="black", command=lambda: (pie_chart_page.pack_forget(), admin_records_page.pack(fill="both", expand=True))).pack(pady=10)

# run the user interface
root.mainloop()