import os
import time
import argparse
import torch
from transformers import GPT2Config, GPT2Model

def load_full():
    # 전체 모델 로드 한줄로 변경 가능 -> partial 로딩과 실험 환경 달라 보류
    # model = AutoModelForCausalLM.from_pretrained("./distilgpt2_model")

    config = GPT2Config.from_pretrained("./distilgpt2_model")

    start = time.time()
    # 부분 모델 인스턴스 생성
    model = GPT2Model(config)
    # 분할된 weight 로딩
    state_path = os.path.join("./distilgpt2_model", "pytorch_model.bin")
    state_dict = torch.load(state_path, map_location="cpu")
    model.load_state_dict(state_dict, strict=False)
    elapsed = time.time() - start
    print(f"🕒 Partial model load time: {elapsed:.4f} seconds")
    return model

def load_partial():
    config = GPT2Config.from_pretrained("./distilgpt2_model")

    start = time.time()
    # 부분 모델 인스턴스 생성
    model = GPT2Model(config)
    # 분할된 weight 로딩
    state_path = os.path.join("./distilgpt2_model", "pytorch_model_part1.bin")
    state_dict = torch.load(state_path, map_location="cpu")
    model.load_state_dict(state_dict, strict=False)
    elapsed = time.time() - start
    print(f"🕒 Partial model load time: {elapsed:.4f} seconds")
    return model

def main():
    parser = argparse.ArgumentParser(description="Load full or partial DistilGPT2 model and measure load time.")
    parser.add_argument(
        "--mode", choices=["full", "partial"], default="full",
        help="'full' to load the entire model, 'partial' to load a subset of layers"
    )
    parser.add_argument(
        "--part_file", default="pytorch_model_part1.bin",
        help="partial 모드에서 사용할 weight 파일"
    )
    args = parser.parse_args()

    if args.mode == "full":
        load_full()
    else:
        load_partial()

if __name__ == "__main__":
    main()
