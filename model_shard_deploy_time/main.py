# 전체 모델
import time
from transformers import AutoModelForCausalLM

start = time.time()
model = AutoModelForCausalLM.from_pretrained("./distilgpt2_model")
end = time.time()

print(f"🕒 Full model load time: {end - start:.2f} seconds")



# 분할된 모델
# import time
# import torch
# from transformers import GPT2Config, GPT2Model

# # 구조 일부만 유지 (예: 3 layer만)
# config = GPT2Config.from_pretrained("./distilgpt2_model")
# config.n_layer = 3

# start = time.time()

# model = GPT2Model(config)

# # 분할 weight 로딩
# state_dict = torch.load("./distilgpt2_model/pytorch_model_part1.bin", map_location="cpu")
# model.load_state_dict(state_dict, strict=False)

# end = time.time()
# print(f"🕒 Partial model load time: {end - start:.2f} seconds")
