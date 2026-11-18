"""Download the raw data for the project into data/raw/.

The notebook does not run this script. It reads only the small snapshot
in data/, which build_snapshot.py makes from the raw files.

    python download_data.py

The same command is the first stage of the DVC pipeline (dvc repro).
The raw files take about 730 MB, so they are not stored in Git.
"""

import time
from pathlib import Path

import requests

RAW_DIR = Path("data/raw")

# The GitHub sources are pinned to a fixed commit, so a new download gives the same files.
# Eurostat has no versions like this, so its numbers can change when they are revised.
INDEED_COMMIT = "d876002488b4497a50c3cc0a2912da53acc023ae"          # 17 Nov 2026
STACK_OVERFLOW_COMMIT = "9dd5c163b7ec09ce5503f711c37a99dbd80ff3c7"  # 22 Oct 2026
GITHUB_COMMIT = "db6ccdf6a8938e10a4304447e3e302562fda3e64"          # 28 Oct 2026

INDEED = f"https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/{INDEED_COMMIT}"
STACK_OVERFLOW = f"https://media.githubusercontent.com/media/StackExchange/Survey/{STACK_OVERFLOW_COMMIT}/packages/archive"
GITHUB = f"https://raw.githubusercontent.com/github/innovationgraph/{GITHUB_COMMIT}/data"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

# Indeed has data by sector only for these three European countries
INDEED_SECTOR_COUNTRIES = ["DE", "FR", "GB"]
INDEED_COUNTRIES = ["DE", "ES", "FR", "GB", "IE", "IT", "NL"]
SURVEY_YEARS = [2022, 2023, 2024, 2025, 2026]

# Eurostat dataset code -> filter (one value per dimension, separated by dots; empty means all values)
EUROSTAT_QUERIES = {
    # Employed ICT specialists: thousands of people and share of all employment
    "isoc_sks_itspt": "",
    # Recruiting of ICT specialists (incl. hard-to-fill vacancies) in firms with 10+ employees,
    # all activities except agriculture, mining and the financial sector
    "isoc_ske_itrcrn2": "A.GE10.C10-S951_X_K...",
    # Price level index (EU27 = 100) for actual individual consumption
    "prc_ppp_ind_1": "A.PLI_EU27_2020.A01.",
    # Yearly average exchange rate: US dollars for 1 euro
    "ert_bil_eur_a": "A.AVG.NAC.USD",
}


def build_file_list():
    """Return (url, local path) pairs for all raw files."""
    files = [(f"{INDEED}/sector-job-title-examples.csv", RAW_DIR / "indeed" / "sector-job-title-examples.csv")]
    for country in INDEED_COUNTRIES:
        files.append((f"{INDEED}/{country}/aggregate_job_postings_{country}.csv",
                      RAW_DIR / "indeed" / f"aggregate_{country}.csv"))
    for country in INDEED_SECTOR_COUNTRIES:
        files.append((f"{INDEED}/{country}/job_postings_by_sector_{country}.csv",
                      RAW_DIR / "indeed" / f"sector_{country}.csv"))

    for year in SURVEY_YEARS:
        # the 2026 file has a different name
        name = "survey_results_public.csv" if year == 2026 else "results.csv"
        files.append((f"{STACK_OVERFLOW}/{year}/{name}", RAW_DIR / "stackoverflow" / f"so_{year}.csv"))

    for dataset, key in EUROSTAT_QUERIES.items():
        files.append((f"{EUROSTAT}/{dataset}/{key}?format=SDMX-CSV&compressed=false",
                      RAW_DIR / "eurostat" / f"{dataset}.csv"))

    files.append((f"{GITHUB}/languages.csv", RAW_DIR / "github" / "languages.csv"))
    return files


def download(url, path, attempts=3):
    """Save one file to disk. Retry on errors, because the Eurostat API is sometimes slow."""
    path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, attempts + 1):
        try:
            with requests.get(url, stream=True, timeout=300) as response:
                response.raise_for_status()
                with open(path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1_000_000):
                        file.write(chunk)
            return
        except requests.RequestException as error:
            print(f"  attempt {attempt} failed: {error}")
            time.sleep(5 * attempt)
    raise RuntimeError(f"Could not download {url}")


def main():
    for url, path in build_file_list():
        print(f"Downloading {path} ...")
        download(url, path)
        print(f"  {path.stat().st_size / 1_000_000:.1f} MB")


if __name__ == "__main__":
    main()
