# European Tech Job Market

Everyone says that tech jobs are the jobs of the future. But in the last few years I have also read a lot about layoffs and fewer job ads for developers. In this project I use open data to check what really happened with the tech job market in Europe since 2020: which roles are growing, which are not, and what they pay. At the end I compare what I found with a published forecast for the next years.

## Motivation

## Data sources
| Source | What I use it for | License |
|---|---|---|
| [Indeed Hiring Lab](https://github.com/hiring-lab/job_postings_tracker) | How the number of job postings changed since February 2020, by sector (DE, FR, GB) and by country | CC BY 4.0 |
| [Stack Overflow Developer Survey](https://survey.stackoverflow.co/) 2022–2026 | Roles, salaries, remote work, languages and AI use of developers in Europe | ODbL 1.0 |
| [Eurostat](https://ec.europa.eu/eurostat) | ICT specialists in employment, hard-to-fill ICT vacancies, price levels and exchange rates | © European Union, reuse with acknowledgement |
| [GitHub Innovation Graph](https://github.com/github/innovationgraph) | Programming languages used on GitHub, by country | CC0 1.0 |

Versions, filters and license details for every file are in [data/SOURCES.md](data/SOURCES.md).

## Methods

## Project structure
```
├── eu_tech_job_market.ipynb  # the main notebook: analysis, math and results
├── download_data.py          # downloads the raw files into data/raw/ (about 730 MB, not in Git)
├── build_snapshot.py         # keeps European countries and the needed columns
├── dvc.yaml                  # the data pipeline: download -> snapshot
├── dvc.lock                  # MD5 hashes of the exact files used
├── data/                     # the snapshot the notebook reads (13 files, about 6 MB)
│   └── SOURCES.md            # sources, versions and licenses
└── requirements.txt
```

## How to run
Requires Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook eu_tech_job_market.ipynb
```

The notebook reads only the files in `data/`, so it works offline.

### Rebuild the snapshot (optional)
The steps that make `data/` are described as a [DVC](https://dvc.org/) pipeline. To run them again:

```bash
pip install dvc==3.67.1
dvc repro
```

This downloads the raw files, builds the snapshot and writes the MD5 hash of every file to `dvc.lock`. After that, `dvc status` tells you if something differs from the saved version. The GitHub sources are pinned to fixed commits, but Eurostat sometimes revises its numbers, so its files can change.

## Results

## References

## Tools used
