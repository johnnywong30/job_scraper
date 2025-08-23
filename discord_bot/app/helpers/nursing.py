import discord
from pandas import DataFrame

import asyncio

from app.helpers.formatters import format_job_as_discord_msg

AUTO_ARCHIVE_DURATION = 10080  # 7 days


class NursingHelper:
    def __init__(
        self,
        data: DataFrame,
        is_new_grad: bool = False,
    ):
        self.data = data
        self.is_new_grad = is_new_grad

    def job_search_notification(self):
        return f"**{len(self.data)} NEW {'NEW GRAD NURSE' if self.is_new_grad else 'NURSE'} JOBS**"

    async def create_job_search_thread(
        self,
        channel: discord.TextChannel,
        thread_name: str,
    ) -> discord.Thread:
        if not isinstance(channel, discord.TextChannel):
            raise TypeError("Channel must be a TextChannel to create a thread")

        thread = await channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.public_thread,
            auto_archive_duration=AUTO_ARCHIVE_DURATION,
        )

        return thread

    async def generate_job_search_notification(self, thread: discord.Thread):
        for _, row in self.data.iterrows():
            msg = format_job_as_discord_msg(row)
            await thread.send(msg)
            await asyncio.sleep(1)
