import sqlite3
from jobspy import scrape_jobs

DB_NAME = "jobs_data.db"
TABLE_NAME = "jobs"

def scrape_and_store_jobs(search_term: str, location: str, results_wanted: int = 100):
    jobs = scrape_jobs(
        site_name=["linkedin", "indeed", "google"],
        search_term=search_term,
        location=location,
        results_wanted=results_wanted,
        country_indeed=location.lower(),
    )

    if jobs.empty:
        return []

    columns_to_keep = [
        "id",
        "site",
        "title",
        "company",
        "location",
        "date_posted",
        "job_url",
        "is_remote",
        "min_amount",
        "max_amount",
        "currency",
    ]

    jobs_clean = jobs[columns_to_keep]

    conn = sqlite3.connect(DB_NAME)
    jobs_clean.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    conn.close()

    return jobs_clean.to_dict(orient="records")
