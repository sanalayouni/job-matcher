from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def match_jobs(candidate: dict, jobs: list):
    candidate_text = f"""
    Job title: {candidate['job_title']}
    Skills: {' '.join(candidate['skills'])}
    Location: {candidate['location']}
    """

    job_texts = []
    for job in jobs:
        job_texts.append(f"""
        Job title: {job.get('title', '')}
        Company: {job.get('company', '')}
        Location: {job.get('location', '')}
        Work type: {'remote' if job.get('is_remote') else 'on-site'}
        """)

    candidate_embedding = model.encode(candidate_text)
    job_embeddings = model.encode(job_texts)

    scores = cosine_similarity(
        candidate_embedding.reshape(1, -1),
        job_embeddings
    )[0]

    for i, job in enumerate(jobs):
        job["match_score"] = round(float(scores[i]) * 100, 2)

    return sorted(jobs, key=lambda x: x["match_score"], reverse=True)
