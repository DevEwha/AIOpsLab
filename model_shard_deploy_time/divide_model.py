import torch

model_path = "./distilgpt2_model/pytorch_model.bin"
state_dict = torch.load(model_path)

keys = list(state_dict.keys())
split1 = int(len(keys) * 1/3)
split2 = int(len(keys) * 2/3)

part1 = {k: state_dict[k] for k in keys[:split1]}
part2 = {k: state_dict[k] for k in keys[split1:split2]}
part3 = {k: state_dict[k] for k in keys[split2:]}

torch.save(part1, "./distilgpt2_model/pytorch_model_part1.bin")
torch.save(part2, "./distilgpt2_model/pytorch_model_part2.bin")
torch.save(part3, "./distilgpt2_model/pytorch_model_part3.bin")
