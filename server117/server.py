import cv2
import numpy as np
from paddleocr import PaddleOCR
import os
from interval import Interval
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
import os
import re
import socket
import threading
import logging
from datetime import datetime


widgets = None
class Result():
    def __init__(self):
        super().__init__()
        self.folder_path = None  # 选择的图片保存路径
        self.ocr_result = None  # ocr模型处理后的结果，两层的列表
        self.res_string = None
        self.paddle = None

    def set_paddle(self, paddle):
        self.paddle = paddle
        return self.paddle
    def set_folder_path(self,folder_path):
        self.folder_path = folder_path
        return folder_path
    def rec(self):
        f_res = self.folder_path
        if os.path.exists(f_res):
            filepath = f_res
        else:
            print("错误,请正确选择图片路径")
        self.ocr_result = self.paddle.ocr(filepath)  # 此时的ocr_result是三层列表，最内层才是识别到的n个数据
        txt = self.align_text(self.ocr_result[0])
        result = self.result_textlist(txt)
        # 结果输出
        res = ""
        for txt_line in result:
            res += txt_line + '\n'
        self.res_string = res
        return res

    # 得到输出数据
    def result_textlist(self, txt):
        try:
            # print(txt)
            result = []
            for textlist in txt:
                key = ''
                value = ''
                age = ''
                flg = True
                key_value = textlist[1].split('@@')[0]
                # print("key_value:",key_value)
                if (key_value[:2] == "2D" or key_value[:2] == "20" or key_value[:2] == "2O" or key_value[:2] == "2o"):
                    continue
                if re.search(r'\)[a-zA-Z0]', key_value):
                    value = textlist[1].split('@@')[1]
                    key = key_value[:-1]
                    # print("key:",key)
                    # print("value:" ,value)
                    flg = False
                if flg:
                    matches = re.search(r'([^0-9]+)(\d+)', key_value)
                    if matches:
                        key = matches.group(1)
                        value = key_value.split(key)[1]
                        # print("key:",key)
                        # print("value:", value)
                age = textlist[1].split('@@')[-2]
                pattern = r'(\d)w.*d'
                match = re.search(pattern, age)
                if match:
                    for i in age:
                        if (i == 'i' or i == 'l' or i == 'A' or i == 'o' or i == 'O'):
                            age = age.replace('i', '1').replace('l', '1').replace('A', '4').replace('o', '0').replace('O',
                                                                                                                      '0')
                else:
                    age = ' '
                if age.find('%') != -1:
                    age = age.split('%')[1]
                # print("age:", age)
                if key == "HC-(Hadlock)" or key == "HC- (Hadlock)" or key == "HC - (Hadlock)" or key == "HC -(Hadlock)" or key == "HC+(Hadlock)" or key == "HC+ (Hadlock)" or key == "HC +(Hadlock)" or key == "HC + (Hadlock)":
                    key = "HC*(Hadlock)"
                if key == "SPD (Hadlock)" or key == "PD (Hadlock)":
                    key = "BPD(Hadlock)"
                if key == "Cereb(Hl":
                    key = "Cereb(Hill)"

                if (key == None):
                    key = key_value
                key = key.replace(" ", "")
                value = value.replace(" ", "")
                key = key.ljust(13, ' ')
                value = value.ljust(11, ' ')
                result.append(key + "\t" + value + "\t" + age)
            return result
        except Exception as e:
            logging.error(f"An error occurred in result_textlist(): {str(e)}")


    # 按识别的文本框从上到下，从左到右排序
    def align_text(self, res, threshold=0):
        try:
            res.sort(key=lambda i: (i[0][0][0]))  # 按照x排
            already_IN, line_list = [], []
            # print(len(res))
            for i in range(len(res)):  # i当前
                if res[i][0][0] in already_IN:
                    continue
                line_txt = res[i][1][0]
                already_IN.append(res[i][0][0])
                y_i_points = [res[i][0][0][1], res[i][0][1][1], res[i][0][3][1], res[i][0][2][1]]
                min_I_y, max_I_y = min(y_i_points), max(y_i_points)
                curr = Interval(min_I_y + (max_I_y - min_I_y) // 3, max_I_y)
                curr_mid = min_I_y + (max_I_y - min_I_y) // 2

                for j in range(i + 1, len(res)):  # j下一个
                    if res[j][0][0] in already_IN:
                        continue
                    y_j_points = [res[j][0][0][1], res[j][0][1][1], res[j][0][3][1], res[j][0][2][1]]
                    min_J_y, max_J_y = min(y_j_points), max(y_j_points)
                    next_j = Interval(min_J_y, max_J_y - (max_J_y - min_J_y) // 3)

                    if next_j.overlaps(curr) and curr_mid in Interval(min_J_y, max_J_y):
                        line_txt += (res[j][1][0] + "@@")
                        already_IN.append(res[j][0][0])
                        curr = Interval(min_J_y + (max_J_y - min_J_y) // 3, max_J_y)
                        curr_mid = min_J_y + (max_J_y - min_J_y) // 2
                line_list.append((res[i][0][0][1], line_txt))
                # print(line_txt)
            line_list.sort(key=lambda x: x[0])
            return line_list
        except Exception as e:
            logging.error(f"An error occurred in align_text(): {str(e)}")




def get_next_image_name(folder, prefix, extension):
    try:
        # 确保文件夹存在
        if not os.path.exists(folder):
            os.makedirs(folder)

        # 获取当前文件夹下以prefix开头的文件的最大编号
        current_max = 0
        for filename in os.listdir(folder):
            if filename.startswith(prefix) and filename.endswith(f'.{extension}'):
                try:
                    num = int(filename[len(prefix):-len(extension) - 1])
                    if num > current_max:
                        current_max = num
                except ValueError:
                    pass  # 忽略无法转换为数字的文件

        # 返回下一个可用的文件名
        return os.path.join(folder, f'{prefix}{current_max + 1}.{extension}')
    except Exception as e:
        logging.error(f"An error occurred in get_next_image_name(): {str(e)}")

def handle_client(conn, result):
    try:
        def reshape(sp):
            return cv2.imdecode(np.array(bytearray(sp), dtype='uint8'), cv2.IMREAD_UNCHANGED)

        def pictobyte(im):
            return np.array(cv2.imencode('.jpg', im)[1]).tobytes()

        def send_txt_data(conn, result_txt):
            conn.sendall(result_txt.encode())
        picture = b''  # 初始化变量
        piclength = ''

        while True:  # 等待字节长度，存为piclength用于下方核验
            data = conn.recv(2048)  # 接受消息
            if len(data) != 0:  # 去除空消息
                raw = data.decode()
                if 'LEN' in raw:
                    piclength = int(raw.strip('LEN'))
                    conn.send('PICTURE'.encode())  # 给发送端下指令发送图片
                    break

        while True:  # 等待字节长度，存为piclength用于下方核验
            data = conn.recv(2048)
            root = os.getcwd()
            # 获取下一个可用的文件名
            image_filename = os.path.join(root, get_next_image_name('recieve/images', 'img', 'jpg'))
            txt_filename = os.path.join(root, get_next_image_name('recieve/images_info', 'img', 'txt'))
            if len(data) != 0:
                picture += data  # 当接收到的消息不为空时直接加到picture(byte类型)里
                print('\r接收进度' + str(int(len(picture) / piclength * 100)) + '%', end='')  # 计算进度
                if len(picture) == piclength:  # 核验，如果不完整显示出来的会很抽象
                    frame = reshape(picture)
                    # 保存图片到固定路径
                    path = image_filename
                    cv2.imwrite(path, frame)
                    # 记录保存图片的日志
                    log_message = f"{datetime.now()} - save {os.path.basename(image_filename)} in {os.path.dirname(image_filename)}"
                    logging.info(log_message)
                    print("\n图片已保存到:", path)
                    cv2.waitKey(0)

                    path = result.set_folder_path(path)
                    result_txt = result.rec()
                    with open(txt_filename, "w") as file:
                        file.write(result_txt)
                    # 记录保存txt文件的日志
                    log_message = f"{datetime.now()} - save {os.path.basename(txt_filename)} in {os.path.dirname(txt_filename)}"
                    logging.info(log_message)
                    print(result_txt)
                    send_txt_data(conn, result_txt)  # Send the result_txt to the client
                    conn.close()
    except Exception as e:
        print(f"Error in handle_client: {e}")
        logging.error(f"An error occurred in handle_client(): {str(e)}")
        conn.close()


def start_server(result):
    try:
        server = socket.socket()  # 创建TCP服务器
        server.bind(('0.0.0.0', 6000))  # 绑定端口
        server.listen(5)


        print("[*] Server listening on 0.0.0.0:6000")

        while True:
            conn, addr = server.accept()  # 接受TCP连接
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # 使用线程处理每个客户端连接，以便同时处理多个客户端
            client_handler = threading.Thread(target=handle_client, args=(conn,result))
            client_handler.start()
    except Exception as e:
            logging.error(f"An error occurred in  start_server(): {e}")


if __name__ == "__main__":
    try:
        # 配置日志
        log_file = 'server_log.log'
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        # 记录日志
        logging.debug('This is a debug message')
        paddle = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True)# need to run only once to download and load model into memory
        result = Result()
        paddle1 = result.set_paddle(paddle)
        start_server(result)
    except Exception as e:
            logging.error(f"An error occurred in the main application: {e}")
