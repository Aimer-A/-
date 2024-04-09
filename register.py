import tkinter as tk
import uuid
import hashlib
import winreg


def generate_machine_code():
    # Get the MAC address of the first network interface
    mac_address = ":".join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))

    # You can use the MAC address directly as the machine code or perform additional processing if needed
    machine_code = mac_address
    return machine_code


def generate_registration_code(machine_code):
    # 使用简单的哈希算法生成注册码
    registration_code = hashlib.md5(machine_code.encode()).hexdigest()
    return registration_code
print(generate_machine_code())
print(generate_registration_code('7c:b5:66:46:b0:44'))
#
# def save_registration_code_to_registry(machine_code, registration_code):
#     # 将机器码和注册码写入注册表
#     key = winreg.HKEY_CURRENT_USER
#     subkey = r"Software\Recognise"  # 修改为你的应用程序名称
#     access = winreg.KEY_SET_VALUE
#     print(access)
#     try:
#         with winreg.OpenKey(key, subkey, 0, access) as registry_key:
#             print(registry_key)
#             winreg.SetValueEx(registry_key, "MachineCode", 0, winreg.REG_SZ, machine_code)
#             winreg.SetValueEx(registry_key, "RegistrationCode", 0, winreg.REG_SZ, registration_code)
#         print("Registration code saved to registry.")
#     except Exception as e:
#         print(f"Error saving registration code to registry: {e}")
#
#
# def check_registration_code():
#     key = winreg.HKEY_CURRENT_USER
#     subkey = r"Software\Recognise"  # 修改为你的应用程序名称
#     access = winreg.KEY_READ
#
#     try:
#         with winreg.OpenKey(key, subkey, 0, access) as registry_key:
#             machine_code = winreg.QueryValueEx(registry_key, "MachineCode")[0]
#             registration_code = winreg.QueryValueEx(registry_key, "RegistrationCode")[0]
#             return machine_code, registration_code
#     except FileNotFoundError:
#         # Key doesn't exist, so create it
#         winreg.CreateKey(key, subkey)
#         print(f"Registry key '{subkey}' created.")
#         return None, None
#
#
# def show_registration_window():
#     # 创建弹窗界面
#     window = tk.Tk()
#     window.title("Registration")
#
#     label = tk.Label(window, text="Enter Registration Code:")
#     label.pack()
#
#     entry = tk.Entry(window)
#     entry.pack()
#
#     def validate_registration_code():
#         user_input = entry.get()
#         _, correct_registration_code = check_registration_code()
#
#         if user_input == correct_registration_code:
#             print("Registration successful!")
#             window.destroy()
#         else:
#             print("Invalid registration code. Try again.")
#
#     button = tk.Button(window, text="Submit", command=validate_registration_code)
#     button.pack()
#
#     window.mainloop()
#
#
# if __name__ == "__main__":
#     machine_code, registration_code = check_registration_code()
#
#     if machine_code is None or registration_code is None:
#         # 第一次打开文件，生成机器码和注册码，并保存到注册表
#         machine_code = generate_machine_code()
#         print(machine_code)
#         registration_code = generate_registration_code(machine_code)
#         print(registration_code)
#         save_registration_code_to_registry(machine_code, registration_code)
#         print("Machine code and registration code generated. Please register.")
#         show_registration_window()
#     else:
#         # 不是第一次打开文件，检查注册码
#         print("Machine code found. Checking registration code.")
