
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForQuestionAnswering, pipeline
import torch
import ast

def text_generation_model(input_sentence):

    model_name = "Qwen/Qwen2.5-1.5B-Instruct"  
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    inputs = tokenizer(input_sentence, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=200,eos_token_id=tokenizer.eos_token_id)
    sentence_generated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return sentence_generated


def response_generation(context, input_sentence):
    

    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

    question = input_sentence
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
 
    inputs = tokenizer.encode_plus(
        question,
        context,
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(**inputs)

   
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    padding = 25  
    start_index = max(0, start_index)  
    end_index = min(len(inputs.input_ids[0]) - 1, end_index + padding)  

    
    answer = tokenizer.decode(inputs.input_ids[0][start_index : end_index + 1])
    

    return answer


def get_response_LLM_pretrained(input_sentence):

    context = text_generation_model(input_sentence=input_sentence)
    response = response_generation(context=context, input_sentence=input_sentence)

    return response
