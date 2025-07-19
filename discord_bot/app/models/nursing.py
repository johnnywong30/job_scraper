from pandas import DataFrame

from typing import TypedDict


class NursingJobSearch(TypedDict):
    rn_jobs: DataFrame
    num_rn_jobs: int
    new_grad_jobs: DataFrame
    num_new_grad_jobs: int
