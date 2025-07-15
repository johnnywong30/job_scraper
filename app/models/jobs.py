from typing import TypedDict


class Job(TypedDict):
    id: str
    site: str
    job_url: str
    job_url_direct: str
    title: str
    company: str
    location: str
    date_posted: str
    company_url: str
    company_url_direct: str
