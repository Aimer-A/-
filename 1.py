from paddleocr import PaddleOCR
paddle = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=True)# need to run only once to download and load model into memory
ocr_result = paddle.ocr('img.png')  # 此时的ocr_result是三层列表，最内层才是识别到的n个数据
print(ocr_result)