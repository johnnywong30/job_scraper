from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import Field

import os

load_dotenv()


class DiscordBotSettings(BaseSettings):
    app_id: str = Field(default=os.getenv("DISCORD_APP_ID"))
    public_key: str = Field(default=os.getenv("DISCORD_APP_PUBLIC_KEY"))
    token: str = Field(default=os.getenv("DISCORD_APP_TOKEN"))
    nursing_channel: int = Field(default=os.getenv("DISCORD_APP_NURSING_CHANNEL_ID"))
    swe_channel: int = Field(default=os.getenv("DISCORD_APP_SWE_CHANNEL_ID"))
