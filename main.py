import tkinter as tk
import random
from clips import Environment
from tkinter import messagebox

# CLIPS EXPERT SYSTEM
env = Environment()

env.build("""
(deftemplate test1 (slot result))
""")

env.build("""
(deftemplate test2 (slot result))
""")

env.build("""
(deftemplate diagnosis
   (slot level)
   (slot recommendation))
""")

env.build("""
(defrule high-risk
   (test1 (result poor))
   (test2 (result poor))
   =>
   (assert (diagnosis
      (level "High Risk of Alzheimer’s Disease")
      (recommendation "Strongly recommended to seek professional medical assessment."))))
""")

env.build("""
(defrule moderate-risk
   (or
      (test1 (result moderate))
      (test2 (result moderate)))
   =>
   (assert (diagnosis
      (level "Moderate Risk of Alzheimer’s Disease")
      (recommendation "Monitor memory health and consider professional screening."))))
""")

env.build("""
(defrule low-risk
   (test1 (result good))
   (test2 (result good))
   =>
   (assert (diagnosis
      (level "Low Risk of Alzheimer’s Disease")
      (recommendation "No significant cognitive impairment detected."))))
""")

env.build("""
(defrule mixed-risk
   (or
      (and (test1 (result good)) (test2 (result poor)))
      (and (test1 (result poor)) (test2 (result good))))
   =>
   (assert (diagnosis
      (level "Moderate Risk of Alzheimer’s Disease")
      (recommendation
        "One cognitive test indicates impairment. Further monitoring is recommended."))))
""")

# GLOBAL RESULTS
mcq_result = None
game_result = None

# MAIN WINDOW 
root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("760x720")

frames = {}

def show_frame(name):
    frames[name].tkraise()

# PAGE 1: WELCOME 
welcome = tk.Frame(root)
frames["welcome"] = welcome
welcome.place(relwidth=1, relheight=1)

tk.Label(welcome, text="WELCOME!", font=("Arial", 30, "bold")).pack(pady=120)
tk.Button(welcome, text="Start Testing", font=("Arial", 16),
          width=20, command=lambda: show_frame("test1")).pack()

# PAGE 2: TEST 1 (MCQ) 
test1 = tk.Frame(root)
frames["test1"] = test1
test1.place(relwidth=1, relheight=1)

tk.Label(test1, text="TEST 1: Memory Recall Test",
         font=("Arial", 18, "bold")).pack(pady=10)

article = (
    "Anna visited the park on Tuesday and fed the ducks near the fountain. "
    "She lost her red scarf but found it under a bench before going home."
)

article_label = tk.Label(test1, text=article, wraplength=700, font=("Arial", 15))
article_label.pack(pady=10)

root.after(10000, lambda: article_label.config(text="[Article hidden]"))

q1, q2, q3 = tk.StringVar(), tk.StringVar(), tk.StringVar()

def mcq(question, options, var):
    frame = tk.Frame(test1)
    frame.pack(anchor="w", padx=60, pady=6)
    tk.Label(frame, text=question, font=("Arial", 12, "bold")).pack(anchor="w")
    for text, val in options:
        tk.Radiobutton(frame, text=text, variable=var, value=val).pack(anchor="w")

mcq("1. What day did Anna visit the park?",
    [("Monday", "A"), ("Tuesday", "B"), ("Wednesday", "C"), ("Thursday", "D")], q1)

mcq("2. What did Anna feed?",
    [("Fish", "A"), ("Pigeons", "B"), ("Ducks", "C"), ("Squirrels", "D")], q2)

mcq("3. Where was the scarf found?",
    [("At home", "A"), ("In her bag", "B"), ("On a tree", "C"), ("Under a bench", "D")], q3)

def finish_test1():
    global mcq_result

    if not q1.get() or not q2.get() or not q3.get():
        messagebox.showwarning(
            "Incomplete Test",
            "Please answer all 3 questions before proceeding."
        )
        return   

    correct = 0
    if q1.get() == "B":
        correct += 1
    if q2.get() == "C":
        correct += 1
    if q3.get() == "D":
        correct += 1

    if correct <= 1:
        mcq_result = "poor"
    elif correct == 2:
        mcq_result = "moderate"
    else:
        mcq_result = "good"

    start_test2()

tk.Button(test1, text="Done", font=("Arial", 14),
          command=finish_test1).pack(pady=20)

# PAGE 3: TEST 2 (CARD MATCHING)
test2 = tk.Frame(root)
frames["test2"] = test2
test2.place(relwidth=1, relheight=1)

tk.Label(test2, text="TEST 2: Card Matching Test",
         font=("Arial", 18, "bold")).pack(pady=10)

board = tk.Frame(test2)
board.pack(pady=20)

def start_test2():
    show_frame("test2")
    setup_game()

def setup_game():
    global cards, buttons, flipped, matched, attempts, game_result
    attempts = 0
    flipped = []
    matched = []
    game_result = None

    for widget in board.winfo_children():
        widget.destroy()

    cards = ['🍎','🍌','🍇','🍓','🍊','🍒','🍉','🥝'] * 2
    random.shuffle(cards)
    buttons = []

    for i in range(16):
        btn = tk.Button(board, text="❓", width=6, height=3,
                        font=("Arial", 18),
                        command=lambda i=i: flip(i))
        btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        buttons.append(btn)

def flip(i):
    if i in flipped or i in matched:
        return
    buttons[i].config(text=cards[i])
    flipped.append(i)
    if len(flipped) == 2:
        root.after(800, check_match)

def check_match():
    global attempts, game_result
    i, j = flipped
    attempts += 1

    if cards[i] == cards[j]:
        matched.extend([i, j])
        buttons[i].config(state="disabled", bg="lightgreen")
        buttons[j].config(state="disabled", bg="lightgreen")
    else:
        buttons[i].config(text="❓")
        buttons[j].config(text="❓")

    flipped.clear()

    if len(matched) == 16:
        if attempts <= 12:
            game_result = "good"
        elif attempts <= 18:
            game_result = "moderate"
        else:
            game_result = "poor"
        show_frame("result")

# PAGE 4: RESULT
result = tk.Frame(root)
frames["result"] = result
result.place(relwidth=1, relheight=1)

tk.Label(result, text="Overall Result",
         font=("Arial", 20, "bold")).pack(pady=20)

output = tk.Text(result, width=80, height=14)
output.pack()

def run_result():
    output.delete("1.0", tk.END)
    env.reset()
    env.assert_string(f"(test1 (result {mcq_result}))")
    env.assert_string(f"(test2 (result {game_result}))")
    env.run()

    for fact in env.facts():
        if fact.template.name == "diagnosis":
            output.insert(tk.END,
                f"TEST 1: {mcq_result.capitalize()}\n"
                f"TEST 2: {game_result.capitalize()}\n\n"
                f"Assessment:\n{fact['level']}\n\n"
                f"Recommendation:\n{fact['recommendation']}")

tk.Button(result, text="Run Result", font=("Arial", 14),
          command=run_result).pack(pady=10)

# START APPLICATION
show_frame("welcome")
root.mainloop()
