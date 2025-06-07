from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

model_name = "distilgpt2"

# 모델과 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 디렉토리 생성
save_dir = "./distilgpt2_model"
os.makedirs(save_dir, exist_ok=True)

# 모델 state_dict만 저장 (.bin 파일)
torch.save(model.state_dict(), os.path.join(save_dir, "pytorch_model.bin"))

# config.json과 vocab 저장
model.config.to_json_file(os.path.join(save_dir, "config.json"))
tokenizer.save_pretrained(save_dir)
