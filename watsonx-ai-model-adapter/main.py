from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import Any, Dict, Union

app = FastAPI()

class Payload(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]
    project_id: str

MODEL = "google/flan-t5-base"

tokenizer = T5Tokenizer.from_pretrained(MODEL)
model = T5ForConditionalGeneration.from_pretrained(MODEL)

    
@app.get("/")
def read_root():
    return {"Text": "Welcome to the watsonx.ai model adapter for IBM Power! The /text endpoint complies to the watsonx.ai model inferencing API and can serves models to you. See: https://ibm.github.io/watson-machine-learning-sdk/fm_extensions.html"}


# See: https://github.com/watson-developer-cloud/assistant-toolkit/blob/master/integrations/extensions/starter-kits/language-model-watsonx/watsonx-openapi.json
@app.post("/ml/v1-beta/generation/text")
async def create_text(payload: Payload):
    input_ids = tokenizer(payload.input, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)

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

