import tkinter as tk
from tkinter import messagebox
import mysql.connector

# ---------- DB CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123456789", #123456789
        database="university_db"
    )

# ---------- GLOBALS ----------
current_user_email = None
current_permissions = set()

# ---------- AUTH ----------
def login():
    global current_user_email, current_permissions

    email = email_entry.get()
    password = password_entry.get()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.user_id, r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.email=%s AND u.password_hash=%s
    """, (email, password))

    row = cursor.fetchone()
    if not row:
        messagebox.showerror("Error", "Invalid credentials")
        return

    current_user_email = email

    cursor.execute("""
        SELECT p.permission_name
        FROM users u
        JOIN role_permissions rp ON u.role_id = rp.role_id
        JOIN permissions p ON rp.permission_id = p.permission_id
        WHERE u.email=%s
    """, (email,))

    current_permissions = {p[0] for p in cursor.fetchall()}
    conn.close()

    root.destroy()
    open_dashboard(row[1])

# ---------- PERMISSION CHECK ----------
def has_permission(permission):
    return permission in current_permissions

# ---------- STUDENT FUNCTIONS ----------
def view_results():
    if not has_permission("view_results"):
        messagebox.showerror("Denied", "Permission denied")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.course_name, r.marks, r.grade
        FROM users u
        JOIN students s ON u.user_id = s.user_id
        JOIN results r ON s.student_id = r.student_id
        JOIN courses c ON r.course_id = c.course_id
        WHERE u.email=%s
    """, (current_user_email,))

    data = cursor.fetchall()
    conn.close()

    text = "\n".join(f"{c} | {m} | {g}" for c, m, g in data)
    messagebox.showinfo("Results", text or "No results found")

def view_attendance():
    if not has_permission("view_attendance"):
        messagebox.showerror("Denied", "Permission denied")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.course_name, a.date, a.status
        FROM users u
        JOIN students s ON u.user_id = s.user_id
        JOIN attendance a ON s.student_id = a.student_id
        JOIN courses c ON a.course_id = c.course_id
        WHERE u.email=%s
    """, (current_user_email,))

    data = cursor.fetchall()
    conn.close()

    text = "\n".join(f"{c} | {d} | {st}" for c, d, st in data)
    messagebox.showinfo("Attendance", text or "No attendance records")

# ---------- DASHBOARD ----------
def open_dashboard(role):
    win = tk.Tk()
    win.title(f"{role.capitalize()} Dashboard")
    win.geometry("420x320")

    tk.Label(win, text=f"Welcome {role.capitalize()}",
             font=("Arial", 16)).pack(pady=15)

    if role == "student":
        tk.Button(win, text="View Results", width=25,
                  command=view_results).pack(pady=5)
        tk.Button(win, text="View Attendance", width=25,
                  command=view_attendance).pack(pady=5)

    elif role == "faculty":
        tk.Label(win, text="Faculty features demo-only").pack(pady=10)

    elif role == "admin":
        tk.Label(win, text="Admin features demo-only").pack(pady=10)

    win.mainloop()

# ---------- LOGIN UI ----------
root = tk.Tk()
root.title("University Management System")
root.geometry("400x260")

tk.Label(root, text="Login", font=("Arial", 18)).pack(pady=10)

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack()

tk.Button(root, text="Login", command=login, width=15).pack(pady=20)

root.mainloop()
