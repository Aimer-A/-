import logging
import os
import socket
import uuid
import hashlib
import winreg
from tkinter import ttk

import cv2
import numpy as np
from functools import partial
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/31 23:47
@Auth ： ccd
@File ：cc.py.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
from main_ui import *
import ctypes
import sys
# from PyQt5 import QtWidgets, QtGui
# from PyQt5.QtWidgets import QMessageBox
# from PyQt5.QtGui import QIcon, QPen, QPainter
from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QMessageBox
from PySide2.QtGui import QIcon, QPen, QPainter
from PIL import ImageGrab, Image, ImageTk, ImageFilter, ImageEnhance
import os
import subprocess
import tkinter as tk
import fitz
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas

# Set up logging
logging.basicConfig(filename='client_log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
widgets = None

result_folder = "res_mod"

if os.path.exists(result_folder):
    pass
else:
    os.mkdir(result_folder)


def get_screen_scaling():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 对应于 LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return dpi / 96.0  # 假设默认 DPI 为 96
    except Exception as e:
        print(f"错误: {e}")
        return 1.0  # 在出错的情况下默认为 100% 缩放


class Screenshot(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.begin = None
        self.end = None
        # Qt::WindowStaysOnTopHint 置顶窗口
        # Qt::FramelessWindowHint 产生一个无窗口边框的窗口，此时用户无法移动该窗口和改变它的大小
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # setWindowOpacity() 只能作用于顶级窗口，取值为0.0~1.0，0.0为完全透明，1.0为完全不透明
        self.setWindowOpacity(0.5)  # 设置窗口透明度为 0.5
        self.setWindowState(Qt.WindowFullScreen)  # 铺满全屏幕
        self.screen_scaling = get_screen_scaling()
        self.file_path = "screenshot.jpg"
        self.file_path1 = "screenshot1.jpg"
        self.callback = callback

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()
        x1, y1 = self.begin.x() * self.screen_scaling, self.begin.y() * self.screen_scaling
        x2, y2 = self.end.x() * self.screen_scaling, self.end.y() * self.screen_scaling
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        if img.mode == "RGB" and img.getbbox():
            img.save(self.file_path1)
            img = img.convert("L")
            enhancer = ImageEnhance.Contrast(img)
            img.filter(ImageFilter.EDGE_ENHANCE)
            contrast_factor = 1.5  # 可以根据需要调整增强的程度
            enhanced_image = enhancer.enhance(contrast_factor)
            # blurred_image = cv2.GaussianBlur(img, (5, 5), 0)
            # sharpened_image = cv2.addWeighted(blurred_image, 1.5, img, -0.5, 0)
            enhanced_image.save(self.file_path)
            # Execute the callback function
            if self.callback:
                self.callback()
        else:
            with open(self.file_path1, "w"):
                pass  # 这里使用pass语句是因为open函数需要有语句块，但我们不需要在文件中写入任何内容
            print("图像为空")
            if self.callback:
                self.callback()
        # img = img.convert("L")
        # enhancer = ImageEnhance.Contrast(img)
        # img.filter(ImageFilter.EDGE_ENHANCE)
        # contrast_factor = 1.5  # 可以根据需要调整增强的程度
        # enhanced_image = enhancer.enhance(contrast_factor)
        # # blurred_image = cv2.GaussianBlur(img, (5, 5), 0)
        # # sharpened_image = cv2.addWeighted(blurred_image, 1.5, img, -0.5, 0)
        # enhanced_image.save(self.file_path)
        # # Execute the callback function
        # if self.callback:
        #     self.callback()
    def paintEvent(self, event):
        if not self.begin:
            return
        painter = QPainter(self)  # 创建QPainter对象
        # painter.setPen(Qt.green)
        # painter.setPen(Qt.red) #设置画笔的颜色
        pen = QPen(Qt.red)
        pen.setWidth(2)  # 设置画笔的宽度
        painter.setPen(pen)

        # drawRect来绘制矩形，四个参数分别是x,y,w,h
        painter.drawRect(self.begin.x(), self.begin.y(),
                         self.end.x() - self.begin.x(), self.end.y() - self.begin.y())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.screenshot = Screenshot(callback=partial(self.restoreMainWindow))
        self.folder_path = None  # 选择的图片保存路径
        self.res_string = None


        title = "矿大超声图像文字识别软件"
        self.setWindowTitle(title)
        self.setWindowIcon((QIcon("icon.ico")))
        global widgets
        widgets = self.ui

        widgets.recognize.clicked.connect(self.copy)  # 识别
        widgets.screenshot.clicked.connect(self.screen_shot)  # 截屏
        widgets.save_result.clicked.connect(self.save_res)  # 保存
        widgets.print_result.clicked.connect(self.print_res)  # 打印
        widgets.path_slc.clicked.connect(self.path_select)   # 预览

    def rec(self):
        try:
            f_res = self.folder_path
            flag = True  # flag为True表示是截图，为False表示是文件夹下的图片

            # 先判断是不是存在截图
            if os.path.exists(self.screenshot.file_path):
                filepath = self.screenshot.file_path
            else:
                if not f_res:
                    QMessageBox.critical(None, "错误", "请正确选择图片路径")
                else:
                    pa_th = os.path.join(f_res, os.listdir(f_res)[0])
                    filepath = pa_th
                    flag = False

            current_folder_path = os.getcwd()
            path = os.path.join(current_folder_path, filepath)

            def reshape(bytes):  # 将接收到的字节重组为ndarray
                return cv2.imdecode(np.array(bytearray(bytes), dtype='uint8'), cv2.IMREAD_UNCHANGED)

            def pictobyte(img):  # 将ndarray转为字节
                return np.array(cv2.imencode('.jpg', img)[1]).tobytes()  # 注：直用tobytes转换字节数会比较大，影响传输效率

            def sendpicture(data, perlength=512):  # 切开发送，相当于说话大喘气
                times = int(len(data) / perlength)
                for i in range(times):
                    s.sendall(data[i * perlength:(i + 1) * perlength])
                s.sendall(data[times * perlength:len(data)])

            def receive_txt_data(conn):
                data = b''
                while True:
                    chunk = conn.recv(2048)
                    if not chunk:
                        break
                    data += chunk
                return data.decode()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接
            s.connect(('10.13.51.61', 6000))  # 这里连映射的端口，别的映射软件我没试过，但是用nat123一定没毛病
            # s.connect(('127.0.0.1', 6000))  # 这里连映射的端口，别的映射软件我没试过，但是用nat123一定没毛病
            data = pictobyte(cv2.imread(path))
            print(len(data))
            length = 'LEN' + str(len(data))
            s.sendall(length.encode())  # 发送图片字节长度，用于服务器核验

            while True:
                command = s.recv(2048)
                if command.decode() == 'PICTURE':  # 接收到服务器传输指令后再传输，防止发送的长度信息与图片信息撞一起
                    break  # 不然会出现图片永远也显示不了
            sendpicture(data)
            # Receive and print the result_txt from the server
            result_txt = receive_txt_data(s)
            print("Received Result Text:\n", result_txt)
            self.res_string = result_txt

            s.close()
            self.ui.res_show.setText(result_txt)
            # Get the text from self.ui.res_show
            result_txt = self.ui.res_show.toPlainText()
            # Access the clipboard
            clipboard = app.clipboard()

            # Set the text to the clipboard
            clipboard.setText(result_txt)
        except Exception as e:
            logging.error(f"An error occurred in rec(): {str(e)}")


    def copy(self):
        try:
            # Get the text from self.ui.res_show
            result_txt = self.ui.res_show.toPlainText()
            # Access the clipboard
            clipboard = app.clipboard()

            # Set the text to the clipboard
            clipboard.setText(result_txt)
            # 弹出提示框
            QMessageBox.information(self, "提示", "已复制到剪切板")
        except Exception as e:
            logging.error(f"An error occurred in copy(): {str(e)}")
    # 截屏
    def screen_shot(self):
        try:
            file_path = self.screenshot.file_path
            os.remove(file_path)
            with open(file_path, "w"):
                pass  # 这里使用pass语句是因为open函数需要有语句块，但我们不需要在文件中写入任何内容
            self.showMinimized()
            self.ui.pic_show.clear()
            self.ui.res_show.clear()
            self.screenshot.show()
        except Exception as e:
            logging.error(f"An error occurred in screen_shot(): {str(e)}")


    def restoreMainWindow(self):
        # Slot to be called when the screenshot is complete
        try:
            self.showNormal()
            f_res = self.folder_path
            flag = True  # flag为True表示是截图，为False表示是文件夹下的图片

            # 先判断是不是存在截图
            if os.path.exists(self.screenshot.file_path):
                filepath = self.screenshot.file_path1
            else:
                if not f_res:
                    QMessageBox.critical(None, "错误", "请正确选择图片路径")
                else:
                    pa_th = os.path.join(f_res, os.listdir(f_res)[0])
                    filepath = pa_th
                    flag = False
            print('---------------------------------')
            self.rec()
            print('---------------------------------')
            # 自适应显示 由于先scaled缩小图片，所以会导致图片变糊
            self.ui.pic_show.setPixmap(
                QtGui.QPixmap(filepath).scaled(self.ui.pic_show.size(), aspectMode=Qt.KeepAspectRatio))
        except Exception as e:
            logging.error(f"An error occurred in restoreMainWindow(): {str(e)}")

    # 保存识别的结果
    def save_res(self):
        try:
            save_path = QtWidgets.QFileDialog.getSaveFileName(None, "选择保存路径", "./", "*.txt")[0]

            res = self.res_string

            with open(save_path, 'w') as f:
                f.write(res)
        except Exception as e:
            logging.error(f"An error occurred in save_res(): {str(e)}")
    # 打印
    def print_res(self):
        try:
            # 声明一个canvas对象
            cav = canvas.Canvas('./res_mod/ocr_result_pdf.pdf')
            # 下载后simsun字体的存放路径
            # simsun_Font_Path = 'D:\\C\Anaconda\\Lib\\site-packages\\reportlab\\fonts\\simsun.ttf'
            simsun_Font_Path = os.path.join(result_folder, 'simsun.ttf')
            # 可以理解成打包一下字体，方便后续使用，类似dataloader的感觉，但dataloader是可迭代的
            font = ttfonts.TTFont('simsun', filename=simsun_Font_Path)
            # 注册字体
            pdfmetrics.registerFont(font=font)
            # 对canvas对象设置字体,setFont函数三个变量依次为字体名称，字号，行间距
            cav.setFont(psfontname='simsun', size=20, leading=1)
            # 绘制字符串
            # cav.drawString(x=50, y=800, text='诊断结果为：')
            # for i in range(1, 12):
            #     cav.drawString(x=50, y=800 - 25 * i, text=res_list[i - 1])
            cav.drawString(x=50, y=800, text="诊断结果为：")
            num = 0
            res = ""
            for value in self.res_string:
                res += value
                # num = num + 1
                # for i in range(2):
                #     res = res + value[i]
                #     if i == 0:
                #         res = res + ":"
                if value == '\n':
                    num = num + 1
                    cav.drawString(x=50, y=800 - 25 * num, text=res)
                    res = ""

            # cav.drawString(x=50, y=100, text=self.res_string)
            # 保存绘制完成的pdf
            cav.showPage()
            cav.save()
            root = os.getcwd()
            cav_object = open(f'{root}/res_mod/ocr_result_pdf.pdf', 'r')
            cav_address = cav_object.name
            print(cav_address)

            def pdf_preview(pdf_path):
                pdf_doc = fitz.open(pdf_path)
                page = pdf_doc.load_page(0)  # 加载第一页
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # 将pix对象转换为PIL Image对象

                return img

            def show_image(image, pdf_path):
                root = tk.Tk()
                root.title("打印预览")

                canvas = tk.Canvas(root, width=image.width, height=1000)
                canvas.pack()

                photo = ImageTk.PhotoImage(image)
                canvas.create_image(0, 0, anchor=tk.NW, image=photo)

                def print_pdf():
                    if sys.platform.startswith('win32'):
                        print("pdf_path: ", pdf_path)
                        os.startfile(pdf_path, "print")
                    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                        subprocess.run(["lpr", pdf_path])
                    else:
                        print("无法打印：不支持的操作系统")

                print_button = tk.Button(root, text="打印", command=print_pdf)
                print_button.pack()

                root.mainloop()

            image = pdf_preview(cav_address)
            show_image(image, cav_address)
        except Exception as e:
            logging.error(f"An error occurred in print_res(): {str(e)}")

    # 选择路径
    def path_select(self):
        try:
            path = QtWidgets.QFileDialog.getExistingDirectory(None, "选择图片保存路径")
            self.ui.path.setText(path)
            f_path = self.ui.path.text()
            self.folder_path = f_path
        except Exception as e:
            logging.error(f"An error occurred in path_select(): {str(e)}")


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


def save_registration_code_to_registry(machine_code, registration_code):
    try:
        # 尝试打开注册表子键，如果不存在则创建
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Recognise"  # 修改为你的应用程序名称
        access = winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY
        registry_key = winreg.OpenKey(key, subkey, 0, access)
    except FileNotFoundError:
        # 如果子键不存在，创建它
        registry_key = winreg.CreateKey(key, subkey)

    try:
        # 将机器码和注册码写入注册表
        winreg.SetValueEx(registry_key, "MachineCode", 0, winreg.REG_SZ, machine_code)
        winreg.SetValueEx(registry_key, "RegistrationCode", 0, winreg.REG_SZ, registration_code)
        print("Registration code saved to registry.")
    except Exception as e:
        print(f"Error saving registration code to registry: {e}")
    finally:
        winreg.CloseKey(registry_key)


def check_registration_code():
    key = winreg.HKEY_CURRENT_USER
    subkey = r"Software\Recognise"  # 修改为你的应用程序名称
    access = winreg.KEY_READ

    try:
        with winreg.OpenKey(key, subkey, 0, access) as registry_key:
            machine_code = winreg.QueryValueEx(registry_key, "MachineCode")[0]
            registration_code = winreg.QueryValueEx(registry_key, "RegistrationCode")[0]
            return machine_code, registration_code
    except FileNotFoundError:
        return None, None


def show_registration_window(registration_code, machine_code):
    result = None

    def validate_registration_code():
        nonlocal result
        user_input = entry.get()
        correct_registration_code = registration_code

        if user_input == correct_registration_code:
            print("Registration successful!")
            result = True
            window.destroy()
        else:
            show_error_message("Invalid registration code. Try again.")
            print("Invalid registration code. Try again.")

    def on_close():
        nonlocal result
        result = False
        window.destroy()

    def show_error_message(message):
        error_window = tk.Tk()
        error_window.title("Error")

        # Calculate the center position of the screen
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x_coordinate = int((screen_width - 300) / 2)
        y_coordinate = int((screen_height - 150) / 2)

        error_window.geometry(f"300x150+{x_coordinate}+{y_coordinate}")

        error_label = ttk.Label(error_window, text=message, font=("Helvetica", 12), foreground="red")
        error_label.pack(pady=10)

        ok_button = ttk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=10)

    def copy_text(text):
        window.clipboard_clear()
        window.clipboard_append(text)
        window.update()

    window = tk.Tk()
    window.title("Registration")
    window.resizable(False, False)

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 10))
    style.configure("TEntry", font=("Helvetica", 10), padding=5, relief="flat", background="#f0f0f0")
    style.configure("TButton", font=("Helvetica", 10), padding=5)

    # Display client machine code as text and Copy button on the same line
    frame_machine_code = ttk.Frame(window)
    frame_machine_code.pack(pady=10)

    machine_code_label = ttk.Label(frame_machine_code, text=f"Machine Code: {machine_code}")
    machine_code_label.pack(side=tk.LEFT, padx=5)

    machine_code_copy_button = ttk.Button(frame_machine_code, text="Copy", command=lambda: copy_text(machine_code))
    machine_code_copy_button.pack(side=tk.RIGHT, padx=0)

    label = ttk.Label(window, text="Enter Registration Code:")
    label.pack(pady=10)

    entry = ttk.Entry(window)  # Use "*" to hide entered characters
    entry.pack(pady=10)

    button = ttk.Button(window, text="Submit", command=validate_registration_code)
    button.pack(pady=10)

    # Calculate the center position of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width - 300) / 2)
    y_coordinate = int((screen_height - 250) / 2)  # Increased height to accommodate three lines

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.geometry(f"300x250+{x_coordinate}+{y_coordinate}")

    window.mainloop()

    return result


if __name__ == "__main__":
    try:
        machine_code, registration_code = check_registration_code()

        if machine_code is None or registration_code is None:
            # 第一次打开文件，生成机器码和注册码，并保存到注册表
            machine_code = generate_machine_code()
            print(machine_code)
            registration_code = generate_registration_code(machine_code)
            print(registration_code)
            print("Machine code and registration code generated. Please register.")
            x = show_registration_window(registration_code, machine_code)
            print(x)
            if x == True:
                save_registration_code_to_registry(machine_code, registration_code)
                app = QtWidgets.QApplication(sys.argv)
                # app.setWindowIcon(QIcon("icon.ico"))
                Main_Window = MainWindow()
                Main_Window.show()
                sys.exit(app.exec_())
        else:
            # 不是第一次打开文件，检查注册码
            print("Machine code found. Checking registration code.")
            # sys.argv 获取当前执行文件的执行时所在的路径，比方说exe在运行时会解压在一个临时文件夹里，此时获取的便是其在临时文件夹下的绝对路径，而不是exe程序所在的路径
            app = QtWidgets.QApplication(sys.argv)
            # app.setWindowIcon(QIcon("icon.ico"))
            Main_Window = MainWindow()
            Main_Window.show()
            sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"An error occurred in the main application: {str(e)}")