import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load files
with open("candidate.json", "r") as f:
    candidate = json.load(f)

with open("jobs_Python_Developer_Tunisia.json", "r") as f:
    jobs = json.load(f)

# Load embedding model
# This model is fast + very good for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# Candidate text
candidate_text = f"""
Job title: {candidate['job_title']}
Skills: {' '.join(candidate['skills'])}
Location: {candidate['location']}
"""

# Job texts
job_texts = []
for job in jobs:
    text = f"""
    Job title: {job.get('title', '')}
    Company: {job.get('company', '')}
    Location: {job.get('location', '')}
    Work type: {'remote' if job.get('is_remote') else 'on-site'}
    """
    job_texts.append(text)

# Create embeddings
candidate_embedding = model.encode(candidate_text)
job_embeddings = model.encode(job_texts)

# Compute similarity
scores = cosine_similarity(
    candidate_embedding.reshape(1, -1),
    job_embeddings
)[0]

# Attach scores
for i, job in enumerate(jobs):
    job["match_score"] = round(float(scores[i]) * 100, 2)

# Sort results
jobs_sorted = sorted(jobs, key=lambda x: x["match_score"], reverse=True)

# Output
print("\n🔹 Job Matches (AI Embeddings):\n")
for job in jobs_sorted:
    print(f"{job['title']} → {job['match_score']}% match")
