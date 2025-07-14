from dotenv import load_dotenv

from .jobs import JobScrapeSettings
from .discord import DiscordBotSettings


load_dotenv()


class Settings(JobScrapeSettings, DiscordBotSettings):
    pass


CONFIG = Settings()
