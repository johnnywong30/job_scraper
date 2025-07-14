import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import io
import logging
import csv

from config import CONFIG
from scraper.nursing import NursingJobs


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
scheduler = AsyncIOScheduler()


nursing_jobs = NursingJobs()
new_grad_nursing_jobs = NursingJobs(
    search_term="new grad registered nurse in California",
    google_search_term="new grad registered nurse in California since yesterday",
)


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user}")

    await schedule_nursing_job_scrape()


async def schedule_nursing_job_scrape():
    channel = bot.get_channel(CONFIG.nursing_channel)
    if channel:
        log.info("Scheduled nursing job scrape")
        jobs = nursing_jobs.scrape_jobs()
        jobs = nursing_jobs.clean_results(jobs)
        num_jobs = len(jobs)
        log.info(f"Found {num_jobs} nursing jobs")

        if num_jobs == 0:
            await channel.send("I didn't find any jobs - sorry 😔")
            return

        # turn pandas df into csv
        csv_buffer = io.StringIO()
        jobs.to_csv(
            csv_buffer,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar="\\",
            index=False,
        )
        csv_bytes = io.BytesIO(csv_buffer.getvalue().encode("utf-8"))
        csv_bytes.seek(0)
        file = discord.File(fp=csv_bytes, filename="nursing_jobs.csv")
        await channel.send(
            f"I found some jobs! Here are {num_jobs} jobs in this csv:", file=file
        )

    else:
        log.warning("Nursing channel not found - sorry 😔")


def main():
    bot.run(CONFIG.token)


if __name__ == "__main__":
    main()
