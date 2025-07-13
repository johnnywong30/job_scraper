from pandas import DataFrame

from .scrape import Scrape


class NursingJobs(Scrape):

    def __init__(
        self,
        search_term: str = "registered nurse in California",
        google_search_term: str = "registered nurse in California since yesterday",
    ):
        super().__init__()
        self.search_term = search_term
        self.google_search_term = google_search_term

    def scrape_jobs(self):
        return super().scrape_jobs(self.search_term, self.google_search_term)

    def save_as_csv(
        self,
        scrape_results: DataFrame,
        filename: str = "nursing_jobs.csv",
    ):
        super().save_as_csv(scrape_results, filename)

    def clean_results(self, scrape_results: DataFrame):
        return super().clean_results(scrape_results)
