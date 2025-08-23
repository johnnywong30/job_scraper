import discord
from discord.ext import commands, tasks

import logging

from app.config import CONFIG
from app.config.log_config import handler
from app.tasks.nursing import scrape_nursing_jobs
from app.helpers.nursing import NursingHelper

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
        rn_jobs = nursing_job_search["rn_jobs"]
        rn_job_thread_builder = NursingHelper(rn_jobs)
        rn_job_notification = rn_job_thread_builder.job_search_notification()
        rn_job_thread = await rn_job_thread_builder.create_job_search_thread(
            channel, rn_job_notification
        )
        await rn_job_thread_builder.generate_job_search_notification(rn_job_thread)

    # new grad registered nurse jobs
    if not nursing_job_search["num_new_grad_jobs"]:
        await channel.send(
            f"I didn't find any New Grad Registered Nurse jobs - sorry 😔"
        )
    else:
        new_grad_jobs = nursing_job_search["new_grad_jobs"]
        new_grad_thread_builder = NursingHelper(new_grad_jobs, is_new_grad=True)
        new_grad_notification = new_grad_thread_builder.job_search_notification()
        new_grad_thread = await new_grad_thread_builder.create_job_search_thread(
            channel, new_grad_notification
        )
        await new_grad_thread_builder.generate_job_search_notification(new_grad_thread)


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
