import torch
print(torch.__version__)  # 打印torch版本
print(torch.version.cuda)  # 如果有CUDA支持，打印cuda版本；否则打印None