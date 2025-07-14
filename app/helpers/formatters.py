from pandas import DataFrame

from datetime import datetime


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
