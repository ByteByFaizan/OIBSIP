import tkinter as tk
from tkinter import messagebox
import string
import secrets


BLACK = "#000000"
PRUSSIAN_BLUE = "#14213D"
ORANGE = "#FCA311"
ALABASTER = "#E5E5E5"
WHITE = "#FFFFFF"

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"



def calculate_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isalpha() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in SYMBOLS for c in password):
        score += 1

    if score <= 1:
        return "Weak", "#C62828"
    elif score <= 3:
        return "Medium", "#EF6C00"
    elif score == 4:
        return "Strong", "#2E7D32"
    else:
        return "Very Strong", ORANGE


def generate_password():
    try:
        length = int(length_entry.get())
        if length < 6:
            messagebox.showerror("Invalid Length", "Password length must be at least 6.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    if not (letters_var.get() or digits_var.get() or symbols_var.get()):
        messagebox.showerror("Selection Error", "Select at least one character type.")
        return

    excluded = exclude_entry.get()
    pool = ""
    password = []

    if letters_var.get():
        letters = set(string.ascii_letters) - set(excluded)
        if letters:
            pool += "".join(letters)
            password.append(secrets.choice(list(letters)))

    if digits_var.get():
        digits = set(string.digits) - set(excluded)
        if digits:
            pool += "".join(digits)
            password.append(secrets.choice(list(digits)))

    if symbols_var.get():
        symbols = set(SYMBOLS) - set(excluded)
        if symbols:
            pool += "".join(symbols)
            password.append(secrets.choice(list(symbols)))

    if not pool:
        messagebox.showerror("Error", "All selected characters are excluded.")
        return

    while len(password) < length:
        password.append(secrets.choice(pool))

    secrets.SystemRandom().shuffle(password)
    final_password = "".join(password)

    result.set(final_password)
    strength, color = calculate_strength(final_password)
    strength_label.config(text=f"Strength: {strength}", fg=color)


def copy_to_clipboard():
    if result.get():
        root.clipboard_clear()
        root.clipboard_append(result.get())
        messagebox.showinfo("Copied", "Password copied to clipboard successfully.")



root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x540")
root.configure(bg=PRUSSIAN_BLUE)
root.resizable(False, False)


tk.Label(
    root,
    text="Advanced Password Generator",
    font=("Segoe UI", 20, "bold"),
    bg=PRUSSIAN_BLUE,
    fg=ORANGE
).pack(pady=18)


card = tk.Frame(root, bg=ALABASTER)
card.pack(padx=25, pady=10, fill="both")


tk.Label(
    card,
    text="Password Length",
    font=("Segoe UI", 11, "bold"),
    bg=ALABASTER,
    fg=BLACK
).grid(row=0, column=0, sticky="w", padx=20, pady=12)

length_entry = tk.Entry(card, width=12, font=("Segoe UI", 11))
length_entry.grid(row=0, column=1)
length_entry.insert(0, "")


letters_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(card, text="Include Letters (A–Z, a–z)", variable=letters_var, bg=ALABASTER, font=("Segoe UI", 10)).grid(row=1, column=0, columnspan=2, sticky="w", padx=20)
tk.Checkbutton(card, text="Include Numbers (0–9)", variable=digits_var, bg=ALABASTER, font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, sticky="w", padx=20)
tk.Checkbutton(card, text="Include Symbols (!@#$…)", variable=symbols_var, bg=ALABASTER, font=("Segoe UI", 10)).grid(row=3, column=0, columnspan=2, sticky="w", padx=20)


tk.Label(
    card,
    text="Exclude Characters",
    font=("Segoe UI", 11, "bold"),
    bg=ALABASTER,
    fg=BLACK
).grid(row=4, column=0, sticky="w", padx=20, pady=12)

exclude_entry = tk.Entry(card, width=22, font=("Segoe UI", 11))
exclude_entry.grid(row=4, column=1)


def on_hover(e):
    e.widget.config(bg=BLACK, fg=WHITE)

def on_leave(e):
    e.widget.config(bg=ORANGE, fg=BLACK)

generate_btn = tk.Button(
    root,
    text="Generate Password",
    bg=ORANGE,
    fg=BLACK,
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    command=generate_password
)
generate_btn.pack(pady=22)
generate_btn.bind("<Enter>", on_hover)
generate_btn.bind("<Leave>", on_leave)


result = tk.StringVar()
tk.Entry(
    root,
    textvariable=result,
    font=("Consolas", 13),
    justify="center",
    width=36
).pack(pady=6)

strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Segoe UI", 11, "bold"),
    bg=PRUSSIAN_BLUE,
    fg=WHITE
)
strength_label.pack(pady=6)

copy_btn = tk.Button(
    root,
    text="Copy to Clipboard",
    bg=BLACK,
    fg=WHITE,
    font=("Segoe UI", 10),
    cursor="hand2",
    command=copy_to_clipboard
)
copy_btn.pack(pady=10)

root.mainloop()