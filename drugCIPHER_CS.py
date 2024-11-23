import os
import pandas as pd
from sklearn.model_selection import train_test_split
import json
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.DataStructs import TanimotoSimilarity
from utils import load_fingerprint
# ------------------------------------
# CS

df = pd.read_csv("kegg/data_with_atc_kegg.csv")

train, test = train_test_split(df, test_size=0.2, random_state=42)

# Compute fingerprints for train and test drugs
train_fps = {dg_id: load_fingerprint(dg_id) for dg_id in train['dg_id']}
test_fps = {dg_id: load_fingerprint(dg_id) for dg_id in test['dg_id']}

# Calculate Tanimoto similarity for each test drug with all train drugs
similarity_results = []

for test_id, test_fp in test_fps.items():
    similarities = [
        TanimotoSimilarity(test_fp, train_fp)
        for train_id, train_fp in train_fps.items()
    ]
    similarity_results.append(similarities)

# Save the results to a file
output_file = "tanimoto_similarity_results.json"

with open(output_file, "w") as f:
    json.dump(similarity_results, f, indent=4)

print(f"Similarity results saved to {output_file}")


# ------------------------------------