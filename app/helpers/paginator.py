import discord
from pandas import DataFrame

from .formatters import format_jobs_as_discord_msg


class Paginator(discord.ui.View):

    def __init__(self, data: DataFrame, page_size: int = 2):
        super().__init__()
        self.data = data
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = (len(data) - 1) // page_size + 1

    def get_page_content(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_df = self.data.iloc[start:end]
        return format_jobs_as_discord_msg(page_df)

    async def update_message(self, interaction):
        content = self.get_page_content()
        footer = f"Page {self.current_page + 1}/{self.total_pages}"
        await interaction.response.edit_message(
            content=f"{content}\n\n{footer}", view=self
        )

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def previous(self, interaction, button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.defer()  # no action if at first page

    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next(self, interaction, button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.defer()  # no action if at last page
