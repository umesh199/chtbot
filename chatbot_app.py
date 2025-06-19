import tkinter as tk
from tkinter import messagebox
import json
import os

# Path to knowledge base
KB_PATH = "/opt/chatbot/knowledge_base.json"
LOG_FILE = "/opt/chatbot/unanswered_queries.txt"

# Load knowledge base
def load_kb():
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r") as file:
            return json.load(file)
    return {}

# Log unknown query
def log_unknown_query(query):
    with open(LOG_FILE, "a") as file:
        file.write(query + "\n")

# Find an answer
def get_answer(query):
    for q, a in knowledge_base.items():
        if q.lower() in query.lower():
            return a
    log_unknown_query(query)
    return "I'm not sure about that. I've logged your question for review."

# Submit query
def on_submit():
    user_query = entry.get()
    if not user_query:
        messagebox.showwarning("Input Needed", "Please type a question.")
        return
    response = get_answer(user_query)
    chat_log.config(state="normal")
    chat_log.insert(tk.END, f"You: {user_query}\nBot: {response}\n\n")
    chat_log.config(state="disabled")
    entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Internal AI ChatBot")
root.geometry("500x400")

chat_log = tk.Text(root, height=20, state="disabled")
chat_log.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Ask", command=on_submit)
submit_btn.pack()

# Load KB
knowledge_base = load_kb()

root.mainloop()
