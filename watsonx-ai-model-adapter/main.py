from fastapi import FastAPI
from huggingface_hub import login
import os
from pydantic import BaseModel
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, T5Tokenizer, T5ForConditionalGeneration
from typing import Any, Dict, Union

app = FastAPI()

class Payload(BaseModel):
    model_id: str
    input: str
    parameters: Dict[str, Any]
    project_id: str


# See: https://huggingface.co/PygmalionAI/pygmalion-6b/discussions/25
class StoppingSequence(StoppingCriteria):
    def __init__(self, stop_sequences, prompt):
        self.stop_sequences = stop_sequences
        self.prompt=prompt

    def __call__(self, input_ids, scores, **kwargs):
        # Get the generated text as a string
        generated_text = tokenizer.decode(input_ids[0])
        generated_text = generated_text.replace(self.prompt,'')
        # Check if the target sequence appears in the generated text
        for stop_sequence in self.stop_sequences:
            if stop_sequence in generated_text:
                return True  # Stop generation

        return False  # Continue generation

    def __len__(self):
        return 1

    def __iter__(self):
        yield self


MODEL = os.getenv('MODEL', "google/flan-t5-base")
TOKEN = os.getenv('TOKEN', None)

if TOKEN is not None:
  login(token=TOKEN)

tokenizer = None
model = None
if MODEL=="ibm/granite-13b-instruct-v2":
  tokenizer = AutoTokenizer.from_pretrained(MODEL)
  model = AutoModelForCausalLM.from_pretrained(MODEL)
elif MODEL=="ibm/mpt-7b-instruct2":
  model_config = AutoConfig.from_pretrained(MODEL)
  tokenizer = AutoTokenizer.from_pretrained(model_config.tokenizer_name)
  model = AutoModelForCausalLM.from_pretrained(MODEL, config=model_config)
elif MODEL=="Deci/DeciLM-7B" or "Deci/DeciLM-7B-instruct":
  tokenizer = AutoTokenizer.from_pretrained(MODEL)
  model = AutoModelForCausalLM.from_pretrained(MODEL)
elif MODEL=="google/flan-t5-base" or MODEL=="google/flan-t5-xxl":
  tokenizer = T5Tokenizer.from_pretrained(MODEL)
  model = T5ForConditionalGeneration.from_pretrained(MODEL)
elif MODEL=="google/flan-ul2":
  tokenizer = AutoTokenizer.from_pretrained(MODEL)
  model = T5ForConditionalGeneration.from_pretrained(MODEL, torch_dtype=torch.bfloat16)
elif MODEL=="TinyLlama/TinyLlama-1.1B-Chat-v1.0" or MODEL=="meta-llama/Llama-2-7b-hf" or MODEL=="meta-llama/Llama-2-13b-hf" or MODEL=="meta-llama/Llama-2-70b-hf":
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

    params = dict()
    if "decoding_method" in payload.parameters:
        decoding_method = payload.parameters["decoding_method"]
        params["do_sample"] = True if decoding_method=="sample" else False
    if "max_new_tokens" in payload.parameters:
        params["max_new_tokens"] = payload.parameters["max_new_tokens"]
    if "min_new_tokens" in payload.parameters:
        params["min_new_tokens"] = payload.parameters["min_new_tokens"]
    if "repetition_penalty" in payload.parameters:
        params["repetition_penalty"] = payload.parameters["repetition_penalty"]
    if "stop_sequences" in payload.parameters:
        params["stopping_criteria"] = StoppingSequence(payload.parameters["stop_sequences"], payload.input) 
    if "temperature" in payload.parameters:
        params["temperature"] = payload.parameters["temperature"]
    if "top_k" in payload.parameters:
        params["top_k"] = payload.parameters["top_k"]
    if "top_p" in payload.parameters:
        params["top_p"] = payload.parameters["top_p"]

    outputs = model.generate(
        input_ids,
        **params,
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

