import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess

def login():
    key = entry_key.get()
    password = entry_password.get()

    if key == "111" and password == "333":
        messagebox.showinfo("ログイン成功", "ログインに成功しました！")

        # ログイン成功の情報を保存
        data = {
            "login": True,
            "logindata": "BAWNHB6M6_5NQC_K4XEBCQAN_BJ5C76TP_HQYRHEVWUGAMG9LNF8T4VAUZS9ZAU2QZT4U64RLVS4HBXNRXQW6PB97_HE_Q63MX6Z"
        }
        save_login_data(data)

        window.destroy()
        open_new_account_window()
    else:
        messagebox.showerror("ログインエラー", "キーまたはパスワードが間違っています。")
        data = load_login_data()
        if data and data["login"] is True:
            data["logindata"] = "BAWNHB6M6_5NQC_K4XEBCQAN_BJ5C76TP_HQYRHEVWUGAMG9LNF8T4VAUZS9ZAU2QZT4U64RLVS4HBXNRXQW6PB97_HE_Q63MX6Z"
            save_login_data(data)

def save_login_data(data):
    folder_path = "c:/windows/temp/faokura_data"
    file_path = os.path.join(folder_path, "data.json")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_login_data():
    file_path = "c:/windows/temp/faokura_data/data.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data

    return None

def open_new_account_window():
    subprocess.Popen(["python", "new.py"])
    window.destroy()

window = tk.Tk()
window.title("ログイン")
window.geometry("500x300")
window.configure(bg="#2C2C2C")

frame = tk.Frame(window, bg="#2C2C2C")
frame.pack(pady=20)

label_key = tk.Label(frame, text="Key", fg="white", bg="#2C2C2C", font=("メイリオ", 12))
label_key.grid(row=0, column=0, padx=10, pady=5)

entry_key = tk.Entry(frame, font=("メイリオ", 12))
entry_key.grid(row=0, column=1, padx=10, pady=5)

label_password = tk.Label(frame, text="Password", fg="white", bg="#2C2C2C", font=("メイリオ", 12))
label_password.grid(row=1, column=0, padx=10, pady=5)

entry_password = tk.Entry(frame, show="*", font=("メイリオ", 12))
entry_password.grid(row=1, column=1, padx=10, pady=5)

button_login = tk.Button(frame, text="Login", command=login, font=("メイリオ", 12), width=15, bg="#007BFF", fg="white")
button_login.grid(row=2, columnspan=2, padx=10, pady=10)

label_new_account = tk.Label(window, text="新しくアカウントを作成", fg="#0066CC", cursor="hand2", font=("メイリオ", 12), bg="#2C2C2C")
label_new_account.pack(pady=5)
label_new_account.bind("<Button-1>", lambda event: open_new_account_window())

window.mainloop()
