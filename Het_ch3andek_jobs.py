import csv
import sqlite3
from jobspy import scrape_jobs

# --- Ask user input ---
search_term = input("Enter job title (e.g. 'Python Developer'): ").strip()
location = input("Enter location (e.g. 'USA', 'Tunisia', 'France'): ").strip()

# --- Scrape jobs ---
jobs = scrape_jobs(
    site_name=["linkedin", "indeed", "google"], #, "bayt", "naukri"
    search_term=search_term,
    location=location,
    results_wanted=100,
    country_indeed=location.lower(),  # auto match location for Indeed
)

print(f"\n✅ Found {len(jobs)} jobs for '{search_term}' in '{location}'")

# --- Keep only relevant columns ---
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

# --- Save to SQLite ---
db_name = "jobs_data.db"
table_name = "jobs"

conn = sqlite3.connect(db_name)
jobs_clean.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()
print(f"💾 Jobs saved to database: {db_name} (table: {table_name})")

# --- Save to CSV ---
csv_file = f"jobs_{search_term.replace(' ', '_')}_{location.replace(' ', '_')}.csv"
jobs_clean.to_csv(csv_file, quoting=csv.QUOTE_NONNUMERIC, index=False)
print(f"📄 CSV saved as: {csv_file}")

# --- Save to JSON ---
json_file = f"jobs_{search_term.replace(' ', '_')}_{location.replace(' ', '_')}.json"
jobs_clean.to_json(json_file, orient="records", indent=4)
print(f"📄 JSON saved as: {json_file}")
