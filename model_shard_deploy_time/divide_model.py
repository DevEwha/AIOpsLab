import torch
import argparse
import os

def split_model(model_dir, num_parts):
    # 모델 weight 파일 경로
    model_path = os.path.join(model_dir, "pytorch_model.bin")
    # CPU로 로드
    state_dict = torch.load(model_path, map_location="cpu")

    # key 목록 및 분할 경계 계산
    keys = list(state_dict.keys())
    total = len(keys)
    # 분할 지점 인덱스 리스트 (1/num_parts, 2/num_parts, ...)
    splits = [int(total * i / num_parts) for i in range(1, num_parts)]
    boundaries = [0] + splits + [total]

    # 각 파트별로 딕셔너리 생성 및 저장
    for i in range(num_parts):
        start, end = boundaries[i], boundaries[i+1]
        part_dict = {k: state_dict[k] for k in keys[start:end]}
        part_file = os.path.join(model_dir, f"pytorch_model_part{i+1}.bin")
        torch.save(part_dict, part_file)
        print(f"Saved part {i+1}/{num_parts}: {part_file} ({end-start} keys)")


def main():
    parser = argparse.ArgumentParser(
        description="Split model state_dict into multiple parts."
    )
    parser.add_argument(
        "--model_dir", default="./distilgpt2_model",
        help="Directory containing pytorch_model.bin and where parts will be written."
    )
    parser.add_argument(
        "--num_parts", type=int, default=5,
        help="Number of parts to split the model into."
    )
    args = parser.parse_args()

    split_model(args.model_dir, args.num_parts)

if __name__ == "__main__":
    main()
