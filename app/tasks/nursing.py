from app.scraper.nursing import NursingJobs
from app.models.nursing import NursingJobSearch

nursing_jobs = NursingJobs()


def scrape_nursing_jobs():
    # scrape regular registered nurse jobs
    rn_jobs = nursing_jobs.scrape_jobs()
    cleaned_rn_jobs = nursing_jobs.clean_results(rn_jobs)

    # scrape new grad registered nurse jobs
    new_grad_rn_jobs = nursing_jobs.scrape_jobs(
        search_term="new grad registered nurse in California",
        google_search_term="new grad registered nurse in California since yesterday",
    )
    cleaned_new_grad_rn_jobs = nursing_jobs.clean_results(new_grad_rn_jobs)

    jobs = NursingJobSearch(
        rn_jobs=cleaned_rn_jobs,
        num_rn_jobs=len(cleaned_rn_jobs),
        new_grad_jobs=cleaned_new_grad_rn_jobs,
        num_new_grad_jobs=len(cleaned_new_grad_rn_jobs),
    )

    return jobs
