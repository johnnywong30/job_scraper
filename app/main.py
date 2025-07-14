import discord
from discord.ext import commands, tasks

import logging

from config import CONFIG
from scraper.nursing import NursingJobs
from helpers.paginator import Paginator
from helpers.formatters import format_time_now, format_jobs_as_discord_file


import time

# Setup logger
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)-12s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


log = logging.getLogger("AstaBot")
log.setLevel(logging.INFO)
log.propagate = False

# Create handler (e.g., console)
handler = logging.StreamHandler()

# Create formatter
formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

# Assign formatter to handler
handler.setFormatter(formatter)

# Clear existing handlers (optional but clean)
log.handlers.clear()

# Add your custom handler
log.addHandler(handler)


# Discord bot plus scheduler

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


nursing_jobs = NursingJobs()
new_grad_nursing_jobs = NursingJobs(
    search_term="new grad registered nurse in California",
    google_search_term="new grad registered nurse in California since yesterday",
)


@tasks.loop(hours=CONFIG.hours_old)
async def schedule_nursing_job_scrape():
    channel = bot.get_channel(CONFIG.nursing_channel)
    if channel:
        log.info("Scheduled nursing job scrape")

        jobs = nursing_jobs.scrape_jobs()
        jobs = nursing_jobs.clean_results(jobs)
        num_jobs = len(jobs)
        log.info(f"Found {num_jobs} nursing jobs")

        if num_jobs == 0:
            await channel.send(
                f"{format_time_now()} -- I didn't find any jobs - sorry 😔"
            )
            return

        paginator = Paginator(jobs, page_size=3)
        header = f"{format_time_now()}\n **{num_jobs} NEW Nursing Jobs**"
        content = paginator.get_page_content()
        footer = f"Page 1/{paginator.total_pages}"

        csv_file = format_jobs_as_discord_file(jobs)

        await channel.send(
            content=f"{header}\n\n{content}\n\n{footer}", view=paginator, file=csv_file
        )
    else:
        log.warning("Nursing channel not found - sorry 😔")


@tasks.loop(hours=CONFIG.hours_old)
async def schedule_new_grad_nursing_job_scrape():
    channel = bot.get_channel(CONFIG.nursing_channel)
    if channel:
        log.info("Scheduled new grad nursing job scrape")

        jobs = new_grad_nursing_jobs.scrape_jobs()
        jobs = new_grad_nursing_jobs.clean_results(jobs)
        num_jobs = len(jobs)
        log.info(f"Found {num_jobs} new grad nursing jobs")

        if num_jobs == 0:
            await channel.send(
                f"{format_time_now()} -- I didn't find any jobs - sorry 😔"
            )
            return

        paginator = Paginator(jobs, page_size=3)
        header = f"{format_time_now()}\n **{num_jobs} NEW New Grad Nursing Jobs**"
        content = paginator.get_page_content()
        footer = f"Page 1/{paginator.total_pages}"
        await channel.send(
            content=f"{header}\n\n{content}\n\n{footer}", view=paginator, file=csv_file
        )
    else:
        log.warning("Nursing channel not found - sorry 😔")


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user}")
    schedule_new_grad_nursing_job_scrape.start()
    schedule_nursing_job_scrape.start()


@bot.event
async def on_disconnect():
    # Cancel loops on disconnect for clean shutdown
    schedule_new_grad_nursing_job_scrape.cancel()
    schedule_nursing_job_scrape.cancel()
    log.info("AstaBot disconnected")


def main():
    bot.run(CONFIG.token)


if __name__ == "__main__":
    main()
