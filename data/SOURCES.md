# Data sources and licenses

The files in this folder were made on **18 November 2026** by `download_data.py` and `build_snapshot.py`.
They contain only 31 European countries (EU27, United Kingdom, Switzerland, Norway, Iceland) and only the columns the notebook needs. No values were changed.

| File | Source and version | License |
|---|---|---|
| `indeed_sectors.csv.gz`, `indeed_totals.csv.gz`, `indeed_sector_examples.csv` | Indeed Hiring Lab, Job Postings Index, https://github.com/hiring-lab/job_postings_tracker, commit `d876002` (17 Nov 2026) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source: Indeed Hiring Lab |
| `stackoverflow_2022.csv.gz` … `stackoverflow_2026.csv.gz` | Stack Overflow Annual Developer Survey, https://survey.stackoverflow.co/, archive commit `9dd5c16` (22 Oct 2026) | [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), contents under [DbCL 1.0](https://opendatacommons.org/licenses/dbcl/1-0/) |
| `eurostat_ict_specialists.csv` | Eurostat, `isoc_sks_itspt`: employed ICT specialists | © European Union, reuse allowed if the source is acknowledged ([copyright notice](https://ec.europa.eu/eurostat/help/copyright-notice)) |
| `eurostat_ict_vacancies.csv` | Eurostat, `isoc_ske_itrcrn2`: firms with 10+ employees that recruited ICT specialists, including hard-to-fill vacancies (all activities except agriculture, mining and the financial sector) | © European Union, as above |
| `eurostat_price_levels.csv` | Eurostat, `prc_ppp_ind_1`: price level index for actual individual consumption, EU27 = 100 | © European Union, as above |
| `eurostat_usd_rates.csv` | Eurostat, `ert_bil_eur_a`: yearly average of US dollars for 1 euro | © European Union, as above |
| `github_languages.csv.gz` | GitHub Innovation Graph, https://github.com/github/innovationgraph, commit `db6ccdf` (28 Oct 2026) | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) |

Changes made to the original files: rows were filtered (countries; only "total postings" for Indeed) and some columns were removed. For the Eurostat files, the removed code columns had only one value after filtering; that value is written in the table above.

The Stack Overflow files are a subset of the original database, so they are shared under the same license (ODbL 1.0).
Stack Overflow publishes the survey as anonymous data. I also removed all free-text answers.

The three GitHub repositories are pinned to the commits above, so `download_data.py` always gets the same files from them.
Eurostat has no such versions and sometimes revises its numbers, so a new download can be different.
The MD5 hash of every file used here is saved in `dvc.lock`.
