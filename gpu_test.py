import torch
print(torch.cuda.is_available())   # Should print: True
print(torch.cuda.get_device_name(0))  # Should print: NVIDIA GeForce RTX 3050
