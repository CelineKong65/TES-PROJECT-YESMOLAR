import tkinter as tk
import random
from clips import Environment

# =========================
# GLOBAL RESULTS
# =========================
mcq_result = None
game_result = None

# =========================
# CLIPS ENVIRONMENT
# =========================
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
   (declare (salience 30))
   (test1 (result poor))
   (test2 (result poor))
   =>
   (assert (diagnosis
      (level "High Risk of Alzheimer’s Disease")
      (recommendation
        "Strongly recommended to seek professional medical assessment."))))
""")

env.build("""
(defrule low-risk
   (declare (salience 25))
   (test1 (result good))
   (test2 (result good))
   =>
   (assert (diagnosis
      (level "Low Risk of Alzheimer’s Disease")
      (recommendation
        "No significant cognitive impairment detected."))))
""")

env.build("""
(defrule moderate-risk
   (declare (salience 20))
   (or
      (test1 (result moderate))
      (test2 (result moderate)))
   =>
   (assert (diagnosis
      (level "Moderate Risk of Alzheimer’s Disease")
      (recommendation
        "Monitor memory health and consider professional screening."))))
""")

env.build("""
(defrule default-result
   (declare (salience -10))
   (not (diagnosis))
   =>
   (assert (diagnosis
      (level "Inconclusive Result")
      (recommendation
        "The assessment results are insufficient for a clear conclusion."))))
""")

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Rule-Based Alzheimer’s Expert System")
root.geometry("750x720")

frames = {}

def show_frame(name):
    frames[name].tkraise()

# =========================
# PAGE 1: WELCOME
# =========================
welcome = tk.Frame(root)
frames["welcome"] = welcome
welcome.place(relwidth=1, relheight=1)

tk.Label(welcome, text="WELCOME!", font=("Arial", 30, "bold")).pack(pady=100)
tk.Button(welcome, text="Start Testing", font=("Arial", 16),
          width=20, command=lambda: show_frame("test1")).pack()

# =========================
# PAGE 2: TEST 1 – MCQ
# =========================
test1 = tk.Frame(root)
frames["test1"] = test1
test1.place(relwidth=1, relheight=1)

tk.Label(test1, text="TEST 1: Memory Recall Test",
         font=("Arial", 18, "bold")).pack(pady=10)

article = (
    "Ali went to the market on Monday morning to buy apples, bread, and milk. "
    "After shopping, he visited his friend Ahmad and returned home by bus."
)

article_label = tk.Label(test1, text=article,
                         wraplength=700, font=("Arial", 12))
article_label.pack(pady=10)

root.after(10000, lambda: article_label.config(
    text="[The article is now hidden]"))

q1, q2, q3 = tk.StringVar(), tk.StringVar(), tk.StringVar()

def mcq_block(question, options, var):
    frame = tk.Frame(test1)
    frame.pack(anchor="w", padx=60, pady=5)
    tk.Label(frame, text=question,
             font=("Arial", 12, "bold")).pack(anchor="w")
    for text, val in options:
        tk.Radiobutton(frame, text=text,
                       variable=var, value=val).pack(anchor="w")

mcq_block("1. What day did Ali go to the market?",
          [("Monday", "correct"), ("Sunday", "wrong")], q1)
mcq_block("2. What did Ali buy?",
          [("Apples, bread, and milk", "correct"), ("Rice and chicken", "wrong")], q2)
mcq_block("3. How did Ali return home?",
          [("Bus", "correct"), ("Car", "wrong")], q3)

def finish_test1():
    global mcq_result
    correct = sum(1 for q in (q1.get(), q2.get(), q3.get()) if q == "correct")

    mcq_result = "poor" if correct <= 1 else "moderate" if correct == 2 else "good"
    show_frame("test2")

tk.Button(test1, text="Done", font=("Arial", 14),
          command=finish_test1).pack(pady=20)

# =========================
# PAGE 3: TEST 2 – CARD MATCHING
# =========================
test2 = tk.Frame(root)
frames["test2"] = test2
test2.place(relwidth=1, relheight=1)

tk.Label(test2, text="TEST 2: Card Matching Memory Test",
         font=("Arial", 18, "bold")).pack(pady=10)

cards = ['🍎', '🍌', '🍇', '🍓', '🍊', '🍈'] * 2
random.shuffle(cards)

buttons, flipped, matched = [], [], []
attempts = 0

board = tk.Frame(test2)
board.pack(pady=20)

def flip_card(i):
    if i in flipped or i in matched:
        return
    buttons[i].config(text=cards[i])
    flipped.append(i)
    if len(flipped) == 2:
        test2.after(800, check_match)

def check_match():
    global attempts, game_result
    i, j = flipped
    attempts += 1

    if cards[i] == cards[j]:
        matched.extend([i, j])
        buttons[i].config(bg="lightgreen", state="disabled")
        buttons[j].config(bg="lightgreen", state="disabled")
    else:
        buttons[i].config(text="❓")
        buttons[j].config(text="❓")

    flipped.clear()

    if len(matched) == 12:
        game_result = "good" if attempts <= 6 else "moderate" if attempts <= 9 else "poor"
        show_frame("result")

for i in range(12):
    btn = tk.Button(board, text="❓", width=6, height=3,
                    font=("Arial", 18),
                    command=lambda i=i: flip_card(i))
    btn.grid(row=i//4, column=i % 4, padx=5, pady=5)
    buttons.append(btn)

# =========================
# PAGE 4: RESULT PAGE
# =========================
result = tk.Frame(root)
frames["result"] = result
result.place(relwidth=1, relheight=1)

tk.Label(result, text="Overall Result",
         font=("Arial", 20, "bold")).pack(pady=20)

result_text = tk.Text(result, height=14, width=80)
result_text.pack(pady=10)

def run_result():
    result_text.delete("1.0", tk.END)

    env.reset()
    env.assert_string(f"(test1 (result {mcq_result}))")
    env.assert_string(f"(test2 (result {game_result}))")
    env.run()

    for fact in env.facts():
        if fact.template.name == "diagnosis":
            result_text.insert(
                tk.END,
                f"TEST 1 (MCQ Memory Test): {mcq_result.capitalize()}\n"
                f"TEST 2 (Card Matching Test): {game_result.capitalize()}\n\n"
                f"Overall Assessment:\n{fact['level']}\n\n"
                f"Recommendation:\n{fact['recommendation']}"
            )

tk.Button(result, text="Run Result",
          font=("Arial", 14), width=20,
          command=run_result).pack(pady=10)

# =========================
# START APPLICATION
# =========================
show_frame("welcome")
root.mainloop()
