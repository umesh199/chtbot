import tkinter as tk
from tkinter import messagebox
import json
import os

# File paths
KB_PATH = "/opt/chatbot/knowledge_base.json"
KEYWORDS_FILE = "/opt/chatbot/issue_keywords.json"
LOG_FILE = "/opt/chatbot/unanswered_queries.txt"

# Load knowledge base
def load_kb():
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r") as file:
            return json.load(file)
    return {}

# Load keyword rules
def load_keywords():
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r") as file:
            return json.load(file)
    return []

# Log unknown queries
def log_unknown_query(query):
    with open(LOG_FILE, "a") as file:
        file.write(query + "\n")

# Permission denied check
def check_permission_issue(query):
    for word in query.split():
        if word.startswith("/") and os.path.exists(word):
            if os.access(word, os.R_OK):
                return f"You have read access to {word}."
            else:
                return f"Permission denied on {word}. Try: sudo chmod o+rx {word}"
    return "Permission denied detected, but no valid folder path found. Please include the full folder path."

# Smart answer engine
def get_answer(query):
    lowered = query.lower()

    # Match keyword rules
    for rule in keyword_rules:
        for keyword in rule.get("keywords", []):
            if keyword in lowered:
                return rule.get("response", "")

    # Permission denied handling
    if "permission denied" in lowered:
        return check_permission_issue(query)

    # Fallback: match from knowledge base
    for q, a in knowledge_base.items():
        if q.lower() in lowered:
            return a

    # Unknown
    log_unknown_query(query)
    return "I'm not sure about that. I've logged your question for review."

# Submit handler
def on_submit():
    user_query = entry.get()
    if not user_query.strip():
        messagebox.showwarning("Input Needed", "Please type your question.")
        return
    response = get_answer(user_query)
    chat_log.config(state="normal")
    chat_log.insert(tk.END, f"You: {user_query}\nBot: {response}\n\n")
    chat_log.config(state="disabled")
    chat_log.see(tk.END)
    entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Internal AI ChatBot")
root.geometry("520x420")

chat_log = tk.Text(root, height=20, state="disabled", wrap="word")
chat_log.pack(pady=10, padx=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=5)

submit_btn = tk.Button(root, text="Ask", command=on_submit)
submit_btn.pack()

# Load files
knowledge_base = load_kb()
keyword_rules = load_keywords()

root.mainloop()
