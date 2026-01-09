import tkinter as tk
from tkinter import messagebox
from clips import Environment

# ==============================
# Initialize CLIPS Environment
# ==============================
env = Environment()

# ==============================
# Define Templates
# ==============================
env.build("""
(deftemplate patient
   (slot age)
   (slot family-history)
   (slot forget-events)
   (slot recall-words)
   (slot confused-time)
   (slot daily-activities))
""")

env.build("""
(deftemplate diagnosis
   (slot result)
   (slot explanation))
""")

# ==============================
# Define Rules
# ==============================
env.build("""
(defrule high-risk-alzheimers
   (patient
      (age ?a&:(>= ?a 65))
      (forget-events yes)
      (recall-words yes)
      (confused-time yes)
      (daily-activities yes))
   =>
   (assert (diagnosis
      (result "High Risk of Alzheimer’s Disease")
      (explanation
        "The patient is elderly and shows severe memory loss, confusion, and difficulty in daily activities."))))
""")

env.build("""
(defrule moderate-risk-alzheimers
   (patient
      (forget-events yes)
      (recall-words yes)
      (confused-time yes))
   =>
   (assert (diagnosis
      (result "Moderate Risk of Alzheimer’s Disease")
      (explanation
        "The patient shows multiple cognitive impairments associated with Alzheimer’s symptoms."))))
""")

env.build("""
(defrule low-risk
   (patient
      (forget-events no)
      (recall-words no)
      (confused-time no))
   =>
   (assert (diagnosis
      (result "Low Risk of Alzheimer’s Disease")
      (explanation
        "The patient shows minimal cognitive symptoms related to Alzheimer’s disease."))))
""")

# ==============================
# Tkinter UI
# ==============================
root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("600x550")

tk.Label(
    root,
    text="Rule-Based Expert System for Alzheimer’s Disease",
    font=("Arial", 16, "bold")
).pack(pady=10)

# ------------------------------
# Patient Information
# ------------------------------
patient_frame = tk.LabelFrame(root, text="Patient Information", padx=10, pady=10)
patient_frame.pack(fill="x", padx=20)

tk.Label(patient_frame, text="Age:").grid(row=0, column=0, sticky="w")
age_entry = tk.Entry(patient_frame, width=10)
age_entry.grid(row=0, column=1)

# ------------------------------
# Memory Assessment
# ------------------------------
memory_frame = tk.LabelFrame(root, text="Memory & Cognitive Assessment", padx=10, pady=10)
memory_frame.pack(fill="x", padx=20, pady=10)

forget_events = tk.BooleanVar()
recall_words = tk.BooleanVar()
confused_time = tk.BooleanVar()
daily_activities = tk.BooleanVar()

tk.Checkbutton(memory_frame, text="Frequently forget recent events", variable=forget_events).pack(anchor="w")
tk.Checkbutton(memory_frame, text="Difficulty recalling recent words", variable=recall_words).pack(anchor="w")
tk.Checkbutton(memory_frame, text="Confused about time or place", variable=confused_time).pack(anchor="w")
tk.Checkbutton(memory_frame, text="Difficulty performing daily activities", variable=daily_activities).pack(anchor="w")

# ------------------------------
# Output
# ------------------------------
output_frame = tk.LabelFrame(root, text="Expert System Output", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=20)

output_text = tk.Text(output_frame, height=8)
output_text.pack(fill="both", expand=True)

# ==============================
# Expert System Function
# ==============================
def run_expert_system():
    env.reset()

    age = age_entry.get()
    if not age.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid age.")
        return

    # Assert patient facts
    env.assert_string(f"""
    (patient
        (age {age})
        (family-history no)
        (forget-events {"yes" if forget_events.get() else "no"})
        (recall-words {"yes" if recall_words.get() else "no"})
        (confused-time {"yes" if confused_time.get() else "no"})
        (daily-activities {"yes" if daily_activities.get() else "no"}))
    """)

    # Run inference
    env.run()

    # Retrieve diagnosis
    output_text.delete("1.0", tk.END)
    found = False

    for fact in env.facts():
        if fact.template.name == "diagnosis":
            found = True
            output_text.insert(tk.END, f"Diagnosis:\n{fact['result']}\n\n")
            output_text.insert(tk.END, f"Explanation:\n{fact['explanation']}")

    if not found:
        output_text.insert(tk.END, "No diagnosis could be determined based on the given inputs.")

# ------------------------------
# Buttons
# ------------------------------
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Run Expert System", width=20, command=run_expert_system).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Reset", width=15, command=lambda: root.destroy()).grid(row=0, column=1)

# ------------------------------
# Disclaimer
# ------------------------------
tk.Label(
    root,
    text="Disclaimer: This system is for educational purposes only and not a medical diagnosis tool.",
    fg="gray",
    font=("Arial", 9)
).pack(pady=5)

root.mainloop()
