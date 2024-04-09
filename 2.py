import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
import hashlib
import pyperclip

def generate_registration_code(machine_code):
    registration_code = hashlib.md5(machine_code.encode()).hexdigest()
    return registration_code

def generate_and_display_registration_code():
    machine_code = entry.get()
    if machine_code:
        registration_code = generate_registration_code(machine_code)
        pyperclip.copy(registration_code)  # 只复制注册码到剪贴板
        messagebox.showinfo("注册码", f"已复制注册码到剪贴板:\n{registration_code}")
    else:
        messagebox.showerror("错误", "请输入机器码")

# 创建主窗口
window = tk.Tk()
window.title("注册码生成器")

# 创建标签
label = Label(window, text="输入机器码:")
label.pack(pady=10)

# 创建输入框
entry = Entry(window)
entry.pack(pady=10)

# 创建按钮
button = Button(window, text="生成注册码", command=generate_and_display_registration_code)
button.pack(pady=10)

# 运行主循环
window.mainloop()
