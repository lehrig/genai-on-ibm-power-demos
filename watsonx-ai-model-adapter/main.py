from fastapi import FastAPI
from huggingface_hub import login
import os
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, T5Tokenizer, T5ForConditionalGeneration
from typing import Any, Dict, Union

app = FastAPI()

class Payload(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]
    project_id: str

MODEL = os.getenv('MODEL', "google/flan-t5-base")
TOKEN = os.getenv('TOKEN', None)

if TOKEN is not None:
  login(token=TOKEN)

tokenizer = None
model = None
if MODEL=="google/flan-t5-base" or MODEL=="google/flan-t5-xxl":
  tokenizer = T5Tokenizer.from_pretrained(MODEL)
  model = T5ForConditionalGeneration.from_pretrained(MODEL)
elif MODEL=="google/flan-ul2":
  tokenizer = AutoTokenizer.from_pretrained(MODEL)
  model = T5ForConditionalGeneration.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
elif MODEL=="meta-llama/Llama-2-7b-hf" or MODEL=="meta-llama/Llama-2-13b-hf" or MODEL=="meta-llama/Llama-2-70b-hf":
  tokenizer = AutoTokenizer.from_pretrained(MODEL)
  model = AutoModelForCausalLM.from_pretrained(MODEL)
else:
  raise ValueError(f'Trying to load unsupported model: {MODEL}.')
    
@app.get("/")
def read_root():
    return {"Text": "Welcome to the watsonx.ai model adapter for IBM Power! The /text endpoint complies to the watsonx.ai model inferencing API and can serve models to you. See: https://ibm.github.io/watson-machine-learning-sdk/fm_extensions.html"}


# See: https://github.com/watson-developer-cloud/assistant-toolkit/blob/master/integrations/extensions/starter-kits/language-model-watsonx/watsonx-openapi.json
@app.post("/ml/v1-beta/generation/text")
async def create_text(payload: Payload):
    input_ids = tokenizer(payload.input, return_tensors="pt").input_ids
    max_new_tokens = payload.parameters["max_new_tokens"]
    min_new_tokens = payload.parameters["min_new_tokens"]
    repetition_penalty = payload.parameters["repetition_penalty"]

    outputs = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        min_new_tokens=min_new_tokens,
        repetition_penalty=repetition_penalty,
    )

    generated_text = tokenizer.decode(outputs[0])
    generated_token_count = outputs.shape[1]
    input_token_count = input_ids.shape[1]
    stop_reason = 'EOS_TOKEN'

    #generated_text = f"Response failed with error '{str(e)}' on prompt '{payload['input']}'"
    #stop_reason = 'ERROR'

    return {
        'results': [{
            'generated_text': generated_text,
            'generated_token_count': generated_token_count,
            'input_token_count': input_token_count,
            'stop_reason': stop_reason}]
    }

