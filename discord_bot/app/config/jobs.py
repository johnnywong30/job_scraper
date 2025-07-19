from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field
from jobspy import Site

from typing import List
import os

load_dotenv()

IS_DOCKER = os.getenv("IS_DOCKER", False)
PROXY_PREFIX = "http://host.docker.internal" if IS_DOCKER else "http://localhost"


class JobScrapeSettings(BaseSettings):
    proxies: List[str] = Field(
        default=[
            f"{PROXY_PREFIX}:3128",
            f"{PROXY_PREFIX}:8080",
            f"{PROXY_PREFIX}:8888",
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
