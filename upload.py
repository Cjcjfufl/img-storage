import os
import subprocess
import shutil
from datetime import datetime

# 仓库路径（当前目录）
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(REPO_DIR, "images")

def get_repo_size(path=IMAGE_DIR):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

def add_image(local_path):
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    
    filename = os.path.basename(local_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"{timestamp}_{filename}"
    target_path = os.path.join(IMAGE_DIR, new_name)
    
    # 拷贝图片到仓库
    shutil.copy(local_path, target_path)
    
    # 检查 5GB 限制
    if get_repo_size() > 5 * 1024**3:
        os.remove(target_path)
        print("⚠️ 超过 5GB 限制，上传失败")
        return
    
    # git 操作
    subprocess.run(["git", "-C", REPO_DIR, "add", target_path], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Add {new_name}"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)
    
    url = f"https://raw.githubusercontent.com/Cjcjfufl/img-storage/main/images/{new_name}"
    print(f"✅ 上传成功，访问链接: {url}")

# 示例：上传 test.jpg
# add_image("test.jpg")
