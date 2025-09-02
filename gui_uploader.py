import os
import subprocess
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# ==== 配置 ====
GITHUB_USERNAME = "Cjcjfufl"     # 改成你的 GitHub 用户名
REPO_NAME = "img-storage"         # 你的仓库名
BRANCH = "main"                   # 默认分支

# 仓库路径（假设脚本放在仓库根目录）
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(REPO_DIR, "images")

# ==== 函数 ====
def get_repo_size(path=IMAGE_DIR):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

def upload_image(local_path):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    filename = os.path.basename(local_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{timestamp}_{filename}"
    target_path = os.path.join(IMAGE_DIR, new_name)
    
    # 拷贝文件
    shutil.copy(local_path, target_path)

    # 检查 5GB 限制
    if get_repo_size() > 5 * 1024**3:
        os.remove(target_path)
        raise Exception("⚠️ 超过 5GB 限制，上传失败")

    # Git 提交
    subprocess.run(["git", "-C", REPO_DIR, "add", target_path], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Add {new_name}"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)

    # 生成 URL
    url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}/images/{new_name}"
    return url

# ==== 图形界面 ====
def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def start_upload():
    file_path = entry_path.get()
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("错误", "请选择有效的图片文件")
        return
    try:
        url = upload_image(file_path)
        messagebox.showinfo("成功", f"上传成功！\n图片地址:\n{url}")
    except Exception as e:
        messagebox.showerror("上传失败", str(e))

# ==== 主窗口 ====
root = tk.Tk()
root.title("GitHub 图床上传器 (5GB 限制)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

label = tk.Label(frame, text="选择图片文件：")
label.pack(anchor="w")

entry_path = tk.Entry(frame, width=50)
entry_path.pack(side="left", padx=5, pady=5)

btn_browse = tk.Button(frame, text="浏览...", command=choose_file)
btn_browse.pack(side="left", padx=5)

btn_upload = tk.Button(root, text="上传到 GitHub", command=start_upload, bg="lightblue")
btn_upload.pack(pady=10)

root.mainloop()

