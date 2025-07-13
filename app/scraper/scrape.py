from jobspy import scrape_jobs
from pandas import DataFrame

import csv
from typing import List

from config import CONFIG


class Scrape:
    def __init__(
        self,
        location: str = CONFIG.location,
        country_indeed: str = CONFIG.country_indeed,
        proxies: List[str] = CONFIG.proxies,
        job_boards: List[str] = CONFIG.job_boards,
        job_type: str = CONFIG.job_type,
        is_remote: bool = CONFIG.is_remote,
        results_wanted: int = CONFIG.results_wanted,
        hours_old: int = CONFIG.hours_old,
    ):
        self.location = location
        self.country_indeed = country_indeed
        self.proxies = proxies
        self.job_boards = job_boards
        self.job_type = job_type
        self.is_remote = is_remote
        self.results_wanted = results_wanted
        self.hours_old = hours_old

    def scrape_jobs(self, search_term: str, google_search_term: str):
        return scrape_jobs(
            site_name=self.job_boards,
            search_term=search_term,
            google_search_term=google_search_term,
            location=self.location,
            results_wanted=self.results_wanted,
            hours_old=self.hours_old,
            country_indeed=self.country_indeed,
            proxies=self.proxies,
            job_type=self.job_type,
            is_remote=self.is_remote,
        )

    def save_as_csv(self, scrape_results: DataFrame, filename: str = "jobs.csv"):
        ####
        # the full set of columns are
        # "id","site","job_url","job_url_direct","title","company","location","date_posted","job_type",
        # "salary_source","interval","min_amount","max_amount","currency","is_remote","job_level",
        # "job_function","listing_type","emails","description","company_industry",
        # "company_url","company_logo","company_url_direct","company_addresses","company_num_employees",
        # "company_revenue","company_description","skills","experience_range","company_rating",
        # "company_reviews_count","vacancy_count","work_from_home_type"
        ####

        scrape_results.to_csv(
            filename,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar="\\",
            index=False,
        )

    def clean_results(self, scrape_results: DataFrame):
        selected_columns = [
            "id",
            "site",
            "job_url",
            "job_url_direct",
            "title",
            "company",
            "location",
            "date_posted",
            "company_url",
            "company_url_direct",
        ]
        clean_df = scrape_results[selected_columns]
        return clean_df
