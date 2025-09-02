import tkinter as tk
from tkinter import messagebox
import requests
from packaging import version

# GitHub 上你的 version.txt 文件地址（改成你的真实仓库链接）
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Cjcjfufl/pulse-update/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"

def get_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def get_remote_version():
    try:
        resp = requests.get(REMOTE_VERSION_URL, timeout=5)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return None
    except Exception as e:
        return None

def check_update():
    local = get_local_version()
    remote = get_remote_version()
    
    if remote is None:
        messagebox.showerror("错误", "无法获取远程版本号！")
        return
    
    if version.parse(remote) > version.parse(local):
        messagebox.showinfo("发现新版本", f"本地版本: {local}\n最新版本: {remote}\n请更新！")
    else:
        messagebox.showinfo("检查结果", f"已是最新版本 ({local})")

# ---------------- 界面 ----------------
root = tk.Tk()
root.title("Pulse 更新检查器")
root.geometry("300x150")

label = tk.Label(root, text="点击按钮检查更新", font=("微软雅黑", 12))
label.pack(pady=20)

check_button = tk.Button(root, text="检查更新", command=check_update, font=("微软雅黑", 10))
check_button.pack()

root.mainloop()
