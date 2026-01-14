import tkinter as tk
from tkinter import messagebox
from clips import Environment

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

# MAIN WINDOW
root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("900x700")
root.configure(bg="#F4F6F8")

# FUNCTIONS 
def show_diagnosis_page():
    start_page.pack_forget()
    diagnosis_page.pack(fill="both", expand=True)

def admin_login():
    messagebox.showinfo(
        "Admin Login",
        "Admin access is restricted.\nFor academic demonstration only."
    )

def diagnose():
    env.reset()

    for code, var in symptom_vars.items():
        if var.get():
            env.assert_string(f"(symptom (code {code}))")

    env.run()

    diagnoses = []

    for fact in env.facts():
        if fact.template.name == "diagnosis":
            diagnoses.append(fact["result"])

    # Priority: Acute > Moderate > Mild
    if "P003" in diagnoses:
        msg = "Diagnosis: Acute Alzheimer’s (P003)"
    elif "P002" in diagnoses:
        msg = "Diagnosis: Moderate Alzheimer’s (P002)"
    elif "P001" in diagnoses:
        msg = "Diagnosis: Mild Alzheimer’s (P001)"
    else:
        msg = "No Alzheimer’s stage detected."

    messagebox.showinfo(
        "Diagnosis Result",
        msg + "\n\n⚠️ This is a preliminary screening.\nConsult medical professionals."
    )

# START PAGE
start_page = tk.Frame(root, bg="#F4F6F8")
start_page.pack(fill="both", expand=True)

tk.Label(
    start_page,
    text="🧠 Alzheimer’s Disease Screening Expert System",
    font=("Segoe UI", 22, "bold"),
    bg="#F4F6F8"
).pack(pady=60)

tk.Button(
    start_page,
    text="▶ Start Testing",
    font=("Segoe UI", 16, "bold"),
    bg="#28B463",
    fg="white",
    padx=40,
    pady=15,
    command=show_diagnosis_page
).pack(pady=20)

tk.Button(
    start_page,
    text="Admin Login",
    font=("Segoe UI", 10),
    bg="#D5DBDB",
    fg="black",
    padx=15,
    pady=5,
    command=admin_login
).pack(pady=10)

tk.Label(
    start_page,
    text="Educational use only | Rule-Based Expert System | TES6313",
    font=("Segoe UI", 10),
    fg="gray",
    bg="#F4F6F8"
).pack(side="bottom", pady=15)

# DIAGNOSIS PAGE
diagnosis_page = tk.Frame(root, bg="#F4F6F8")

header = tk.Frame(diagnosis_page, bg="#2E86C1", height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="Select Patient Symptoms",
    font=("Segoe UI", 18, "bold"),
    bg="#2E86C1",
    fg="white"
).pack(pady=20)

card = tk.Frame(diagnosis_page, bg="white")
card.pack(padx=40, pady=20, fill="both", expand=True)

canvas = tk.Canvas(card, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
symptom_frame = tk.Frame(canvas, bg="white")

canvas.create_window((0, 0), window=symptom_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
scrollbar.pack(side="right", fill="y", padx=(0, 20))

symptom_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

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
    tk.Checkbutton(
        symptom_frame,
        text=text,
        variable=symptom_vars[code],
        bg="white",
        font=("Segoe UI", 12),
        anchor="w",
        padx=20
    ).pack(fill="x", pady=4)

tk.Button(
    diagnosis_page,
    text="🔍 Run Diagnosis",
    font=("Segoe UI", 14, "bold"),
    bg="#28B463",
    fg="white",
    padx=20,
    pady=10,
    command=diagnose
).pack(pady=20)

root.mainloop()