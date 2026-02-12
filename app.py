import tkinter as tk
from tkinter import messagebox
import mysql.connector

# ---------- DB CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="", #
        database="university_db"
    )
# ---------- LOGIN LOGIC ----------
def login():
    email = email_entry.get()
    password = password_entry.get()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT r.role_name
        FROM users u
        JOIN roles r ON u.role_id = r.role_id
        WHERE u.email=%s AND u.password_hash=%s
        """
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            role = result[0]
            messagebox.showinfo("Login Success", f"Logged in as {role}")
            root.withdraw()  # Hide login window
            open_dashboard(role)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------- DASHBOARD ----------
def open_dashboard(role):
    dashboard = tk.Toplevel()
    dashboard.title(f"{role.capitalize()} Dashboard")

    # Fullscreen
    dashboard.attributes("-fullscreen", True)

    # Exit fullscreen with ESC
    dashboard.bind("<Escape>", lambda e: dashboard.attributes("-fullscreen", False))

    # Header
    header = tk.Label(dashboard, text=f"Welcome {role.capitalize()}",
                      font=("Arial", 28, "bold"))
    header.pack(pady=40)

    # Buttons Frame
    btn_frame = tk.Frame(dashboard)
    btn_frame.pack(pady=20)

    if role == "student":
        tk.Button(btn_frame, text="View Results",
                  command=view_results, width=25, height=2).pack(pady=10)

        tk.Button(btn_frame, text="View Attendance",
                  command=view_attendance, width=25, height=2).pack(pady=10)

    elif role == "faculty":
        tk.Button(btn_frame, text="Mark Attendance",
                  command=dummy_action, width=25, height=2).pack(pady=10)

        tk.Button(btn_frame, text="Upload Marks",
                  command=dummy_action, width=25, height=2).pack(pady=10)

    elif role == "admin":
        tk.Button(btn_frame, text="Manage Users",
                  command=dummy_action, width=25, height=2).pack(pady=10)

        tk.Button(btn_frame, text="Manage Courses",
                  command=dummy_action, width=25, height=2).pack(pady=10)

    # Logout Button
    tk.Button(dashboard, text="Logout", bg="red", fg="white",
              command=lambda: logout(dashboard),
              width=15, height=2).pack(pady=40)


def logout(dashboard):
    dashboard.destroy()
    root.deiconify()  # Show login window again


# ---------- SAMPLE ACTIONS ----------
def view_results():
    messagebox.showinfo("Results", "Fetching results from database...")


def view_attendance():
    messagebox.showinfo("Attendance", "Fetching attendance from database...")


def dummy_action():
    messagebox.showinfo("Action", "Feature demo only")


# ---------- LOGIN UI ----------
root = tk.Tk()
root.title("University Management System")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Login", font=("Arial", 20, "bold")).pack(pady=15)

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root, width=35)
email_entry.pack(pady=5)

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*", width=35)
password_entry.pack(pady=5)

tk.Button(root, text="Login", command=login,
          width=20, height=2).pack(pady=20)

root.mainloop()
