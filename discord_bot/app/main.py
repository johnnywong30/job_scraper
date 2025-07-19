import discord
from discord.ext import commands, tasks

import logging

from app.config import CONFIG
from app.config.log_config import handler
from app.tasks.nursing import scrape_nursing_jobs
from app.helpers.paginators.nursing import NursingPaginator

# Setup logger with handler
log = logging.getLogger("AstaBot")
log.setLevel(logging.INFO)
log.propagate = False
log.handlers.clear()
log.addHandler(handler)


# Discord bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(minutes=30)
async def schedule_ping():
    await bot.wait_until_ready()
    log.info("Ping bot is awake")


@tasks.loop(hours=CONFIG.hours_old)
async def schedule_nursing_job_scrape():
    await bot.wait_until_ready()
    channel = bot.get_channel(CONFIG.nursing_channel)
    if not channel:
        log.warning("Nursing channel not found - sorry 😔")
        return

    log.info("Queued up nursing job scrape.")
    nursing_job_search = scrape_nursing_jobs()
    # registered nurse jobs
    if not nursing_job_search["num_rn_jobs"]:
        await channel.send(f"I didn't find any Registered Nurse jobs - sorry 😔")
    else:
        rn_paginator = NursingPaginator(nursing_job_search["rn_jobs"], page_size=3)
        await channel.send(
            content=rn_paginator.build_paginator_msg(),
            view=rn_paginator,
            file=rn_paginator.build_nursing_csv_file(),
        )

    # new grad registered nurse jobs
    if not nursing_job_search["num_new_grad_jobs"]:
        await channel.send(
            f"I didn't find any New Grad Registered Nurse jobs - sorry 😔"
        )
    else:
        new_grad_paginator = NursingPaginator(
            nursing_job_search["new_grad_jobs"],
            page_size=3,
            is_new_grad=True,
        )
        await channel.send(
            content=new_grad_paginator.build_paginator_msg(),
            view=new_grad_paginator,
            file=new_grad_paginator.build_nursing_csv_file(),
        )


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user}")
    if not schedule_nursing_job_scrape.is_running():
        log.info("Scheduling new grad nursing job scrape task")
        schedule_nursing_job_scrape.start()
    if not schedule_ping.is_running():
        log.info("Scheduling ping task")
        schedule_ping.start()


@bot.event
async def on_disconnect():
    log.info("Job scrape bot disconnected")


def main():
    bot.run(CONFIG.token)


if __name__ == "__main__":
    main()
