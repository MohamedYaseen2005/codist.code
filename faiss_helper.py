import faiss
import numpy as np
import json
import os

def load_logic_hints(file_path="logic_hints.json"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def save_logic_hints(logic_hints, file_path="logic_hints.json"):
    with open(file_path, "w") as f:
        json.dump(logic_hints, f, indent=2)

def build_faiss_index(hints, embed_fn):
    vectors = [embed_fn(hint) for hint in hints]
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype('float32'))
    return index

def get_closest_hint(user_input, index, hints, embed_fn, threshold=0.5):
    user_vector = np.array([embed_fn(user_input)]).astype('float32')
    distances, indices = index.search(user_vector, 1)
    if distances[0][0] < threshold:
        return hints[indices[0][0]]
    return None