import google.generativeai as genai
import numpy as np
import os
from faiss_helper import *

with open("GOOGLE_API_KEY.txt") as f:
    genai.configure(api_key=f.read().strip())

model = genai.GenerativeModel("gemini-1.5-flash-latest")
embed_model = genai.embed_content

def embed(text):
    res = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return np.array(res["embedding"], dtype="float32")

logic_hints = load_logic_hints()
faiss_index = build_faiss_index(logic_hints, embed)

def generate_hint_from_examples(user_input):
    prompt = f"""
You are a helpful AI that gives hard hints in 10 words or fewer. 
Use these logic samples to guide the hint style:

{json.dumps(logic_hints, indent=2)}

User Logic: {user_input}
Give only one hard hint. Do not explain.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_hint_from_web(user_input):
    prompt = f"""
You are a coding assistant that helps users debug logic.
You couldn't generate a good hint from existing samples.

Now use your web knowledge to give one hard hint (max 10 words) 
that matches the following user problem:

User Logic: {user_input}

The hint must feel similar to:
{json.dumps(logic_hints, indent=2)}

Return only the new hint.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

while True:
    user_input = input("\nEnter your logic statement (or type 'exit'): ").strip()
    if user_input.lower() == "exit":
        break

    # IF: Match in FAISS
    matched_hint = get_closest_hint(user_input, faiss_index, logic_hints, embed)
    if matched_hint:
        print("Hint (from existing):", matched_hint)
        continue

    # ELIF: Generate new hint
    new_hint = generate_hint_from_examples(user_input)
    if new_hint and new_hint not in logic_hints:
        logic_hints.append(new_hint)
        save_logic_hints(logic_hints)
        faiss_index = build_faiss_index(logic_hints, embed)
        print("Hint (generated):", new_hint)
        continue

    # ELSE: Use web knowledge
    web_hint = generate_hint_from_web(user_input)
    if web_hint and web_hint not in logic_hints:
        logic_hints.append(web_hint)
        save_logic_hints(logic_hints)
        faiss_index = build_faiss_index(logic_hints, embed)
        print("Hint (from web):", web_hint)
    else:
        print("Could not generate a suitable hint.")