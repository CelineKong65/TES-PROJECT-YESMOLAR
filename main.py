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

root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("850x650")

tk.Label(root, text="Alzheimer’s Disease Screening",
         font=("Arial", 24, "bold")).pack(pady=10)

tk.Label(root, text="Please select all symptoms that apply:",
         font=("Arial", 14)).pack(pady=5)

# Symptom list
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

vars = {}

frame = tk.Frame(root)
frame.pack(pady=10)

for code, text in symptoms.items():
    vars[code] = tk.BooleanVar()
    tk.Checkbutton(frame, text=text, variable=vars[code],
                   font=("Arial", 11)).pack(anchor="w")

def diagnose():
    env.reset()

    for code, var in vars.items():
        if var.get():
            env.assert_string(f"(symptom (code {code}))")

    env.run()

    result_text = ""
    for fact in env.facts():
        if fact.template.name == "diagnosis":
            if fact["result"] == "P001":
                result_text = "Diagnosis: Mild Alzheimer’s (P001)"
            elif fact["result"] == "P002":
                result_text = "Diagnosis: Moderate Alzheimer’s (P002)"
            elif fact["result"] == "P003":
                result_text = "Diagnosis: Acute Alzheimer’s (P003)"

    if result_text:
        messagebox.showinfo(
            "Diagnosis Result",
            result_text + "\n\n⚠️ This is a preliminary screening.\nPlease consult medical professionals."
        )
    else:
        messagebox.showinfo(
            "Diagnosis Result",
            "No Alzheimer’s stage detected based on selected symptoms."
        )

tk.Button(root, text="Run Diagnosis",
          font=("Arial", 14),
          bg="#4CAF50", fg="white",
          command=diagnose).pack(pady=20)

root.mainloop()
