from fastapi import FastAPI, Request
from transformers import pipeline, AutoTokenizer

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token_id = tokenizer.eos_token_id

generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer=tokenizer
)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return {"error": "prompt 값을 반드시 입력해야 합니다."}

    output = generator(
        prompt,
        max_new_tokens=50,
        truncation=True
    )
    return {"result": output}
