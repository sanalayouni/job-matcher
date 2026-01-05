from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from scraper import scrape_and_store_jobs
from matcher import match_jobs

app = FastAPI(title="AI Job Matcher API")

# ---------- Schemas ----------

class JobSearch(BaseModel):
    title: str
    location: str
    results_wanted: int = 50

class CandidateProfile(BaseModel):
    job_title: str
    skills: List[str]
    location: str

class JobMatcherRequest(BaseModel):
    job_search: JobSearch
    candidate: CandidateProfile

# ---------- Endpoint ----------

@app.post("/job-matcher")
def job_matcher(request: JobMatcherRequest):
    # 1️⃣ Scrape jobs
    jobs = scrape_and_store_jobs(
        request.job_search.title,
        request.job_search.location,
        request.job_search.results_wanted
    )

    if not jobs:
        return {"count": 0, "matches": []}

    # 2️⃣ Match jobs with candidate
    ranked_jobs = match_jobs(
        request.candidate.dict(),
        jobs
    )

    return {
        "count": len(ranked_jobs),
        "matches": ranked_jobs
    }
