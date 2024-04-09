import paddle

yes = paddle.utils.run_check()
print("paddle.utils.run_check:", yes)
gpu_available = paddle.device.is_compiled_with_cuda()
print("GPU available:", gpu_available)
print(paddle.__version__)