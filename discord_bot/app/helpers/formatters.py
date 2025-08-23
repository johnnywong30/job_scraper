from pandas import DataFrame, Series
import discord

from datetime import datetime
import io
import csv


def format_job_as_discord_msg(row: Series):
    return (
        f"**{row['title']}**\n\n"
        f"🏢 {row['company']}   📍 {row['location']}\n"
        f"🔗 <{row['job_url']}>\n\n"
    )


def format_jobs_as_discord_msg(jobs: DataFrame):
    lines = []
    for _, row in jobs.iterrows():
        lines.append(
            f"**{row['title']}**\n\n"
            f"🏢 {row['company']}   📍 {row['location']}\n"
            f"🔗 <{row['job_url']}>\n"
            "–––"
        )

    return "\n".join(lines)


def format_time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_jobs_as_discord_file(jobs: DataFrame):
    csv_buffer = io.StringIO()
    jobs.to_csv(csv_buffer, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    csv_bytes = io.BytesIO(csv_buffer.getvalue().encode("utf-8"))
    csv_bytes.seek(0)

    file = discord.File(fp=csv_bytes, filename="jobs.csv")
    return file
