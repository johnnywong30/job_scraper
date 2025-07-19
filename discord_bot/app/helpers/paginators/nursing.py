from pandas import DataFrame

from app.helpers.paginators.paginator import Paginator
from app.helpers.formatters import format_jobs_as_discord_file


class NursingPaginator(Paginator):

    def __init__(self, data: DataFrame, page_size: int = 2, is_new_grad: bool = False):
        super().__init__(data, page_size)
        self.is_new_grad = is_new_grad

    def build_nursing_header(self):
        return f"**{len(self.data)} NEW {'NEW GRAD NURSE' if self.is_new_grad else 'NURSE'} JOBS**"

    def build_nursing_footer(self):
        return f"Page 1/{self.total_pages}"

    def build_nursing_csv_file(self):
        csv_file = format_jobs_as_discord_file(self.data)
        return csv_file

    async def update_message(self, interaction):
        content = self.get_page_content()
        footer = f"Page {self.current_page + 1}/{self.total_pages}"
        await interaction.response.edit_message(
            content=f"{self.build_nursing_header()}\n\n{content}\n\n{footer}", view=self
        )

    def build_paginator_msg(self):
        return f"{self.build_nursing_header()}\n\n{self.get_page_content()}\n\n{self.build_nursing_footer()}"
