"""Build the small data snapshot in data/ from the raw files in data/raw/.

Only European countries and the columns needed later are kept, so the files
are small enough for GitHub. The values are not cleaned or changed here.
All cleaning and validation is done in the notebook, step by step.

Run it after download_data.py:

    python build_snapshot.py
"""

from pathlib import Path

import pandas as pd

from download_data import INDEED_COUNTRIES, INDEED_SECTOR_COUNTRIES, RAW_DIR, SURVEY_YEARS

OUT_DIR = Path("data")

# EU27 + United Kingdom, Switzerland, Norway and Iceland, named as in the Stack Overflow survey
SURVEY_COUNTRIES = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
    "Spain", "Sweden", "United Kingdom of Great Britain and Northern Ireland", "Switzerland", "Norway",
    "Iceland",
]
# The same 31 countries as ISO 3166 codes, which GitHub uses
ISO_CODES = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT",
    "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "GB", "CH", "NO", "IS",
]
# Eurostat writes EL for Greece and UK for the United Kingdom; EU27_2020 is the EU total
EUROSTAT_CODES = [code for code in ISO_CODES if code not in ("GR", "GB")] + ["EL", "UK", "EU27_2020"]

# Not every column exists in every survey year; each file keeps the ones it has
SURVEY_COLUMNS = [
    "ResponseId", "MainBranch", "Age", "Employment", "RemoteWork", "WorkSetting", "EdLevel", "Education",
    "YearsCode", "YearsCodePro", "WorkExp", "DevType", "Role", "OrgSize", "Industry", "Country",
    "Currency", "CompTotal", "CompFreq", "ConvertedCompYearly", "LanguageHaveWorkedWith",
    "LanguagesHaveWorkedWith", "AISelect", "ICorPM",
]
EUROSTAT_COLUMNS = ["geo", "TIME_PERIOD", "OBS_VALUE", "OBS_FLAG"]

# mtime=0 removes the time stamp from the .gz header, so every run gives identical bytes
GZIP = {"method": "gzip", "mtime": 0}


def save(table, name):
    """Write a table to data/ and print its size."""
    path = OUT_DIR / name
    table.to_csv(path, index=False, compression=GZIP if name.endswith(".gz") else None)
    print(f"{path}: {len(table)} rows, {path.stat().st_size / 1000:.0f} KB")


def build_indeed():
    """Keep 'total postings' (and drop 'new postings') for sectors and country totals; copy the sector examples."""
    sectors = pd.concat(pd.read_csv(RAW_DIR / "indeed" / f"sector_{c}.csv") for c in INDEED_SECTOR_COUNTRIES)
    sectors = sectors[sectors["variable"] == "total postings"].drop(columns="variable")
    save(sectors, "indeed_sectors.csv.gz")

    totals = pd.concat(pd.read_csv(RAW_DIR / "indeed" / f"aggregate_{c}.csv") for c in INDEED_COUNTRIES)
    totals = totals[totals["variable"] == "total postings"].drop(columns="variable")
    save(totals, "indeed_totals.csv.gz")

    save(pd.read_csv(RAW_DIR / "indeed" / "sector-job-title-examples.csv"), "indeed_sector_examples.csv")


def build_survey():
    """One file per year with European respondents only. No free-text answers are kept."""
    for year in SURVEY_YEARS:
        survey = pd.read_csv(RAW_DIR / "stackoverflow" / f"so_{year}.csv",
                             usecols=lambda column: column in SURVEY_COLUMNS, low_memory=False)
        survey = survey[survey["Country"].isin(SURVEY_COUNTRIES)]
        save(survey, f"stackoverflow_{year}.csv.gz")


def build_eurostat():
    """Keep European countries, plus the code columns that still have more than one value."""
    tables = {
        "isoc_sks_itspt": ("eurostat_ict_specialists.csv", ["unit"]),
        "isoc_ske_itrcrn2": ("eurostat_ict_vacancies.csv", ["indic_is", "unit"]),
        "prc_ppp_ind_1": ("eurostat_price_levels.csv", []),
    }
    for dataset, (name, code_columns) in tables.items():
        table = pd.read_csv(RAW_DIR / "eurostat" / f"{dataset}.csv")
        table = table[table["geo"].isin(EUROSTAT_CODES)]
        save(table[code_columns + EUROSTAT_COLUMNS], name)

    rates = pd.read_csv(RAW_DIR / "eurostat" / "ert_bil_eur_a.csv")
    save(rates[["TIME_PERIOD", "OBS_VALUE", "OBS_FLAG"]], "eurostat_usd_rates.csv")


def build_github():
    """Keep European countries. keep_default_na=False, because pandas would read 'NA' (Namibia) as missing."""
    languages = pd.read_csv(RAW_DIR / "github" / "languages.csv", keep_default_na=False)
    save(languages[languages["iso2_code"].isin(ISO_CODES)], "github_languages.csv.gz")


def main():
    build_indeed()
    build_survey()
    build_eurostat()
    build_github()


if __name__ == "__main__":
    main()
