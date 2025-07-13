from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field
from jobspy import Site

from typing import List

load_dotenv()


class Settings(BaseSettings):
    # job scrape settings

    proxies: List[str] = Field(
        default=[
            "http://localhost:3128",
            "http://localhost:8080",
            "http://localhost:8888",
        ],
    )
    job_boards: List[str] = Field(
        default=[
            Site.INDEED.value,
            Site.LINKEDIN.value,
            Site.ZIP_RECRUITER.value,
            Site.GLASSDOOR.value,
            Site.GOOGLE.value,
        ]
    )
    location: str = Field(default="CA")
    country_indeed: str = Field(default="USA")
    job_type: str = Field(default="fulltime")
    is_remote: bool = Field(default=False)
    results_wanted: int = Field(default=20)
    hours_old: int = Field(default=1)


CONFIG = Settings()
