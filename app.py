from pathlib import Path
import sys
import traceback
from discord.ext import commands
import os

client = commands.Bot(command_prefix="$",description="test bot")

def load_cogs_from_system(client, target_dir): 
    [client.load_extension(f"cogs.{file.stem}") for file in Path(target_dir).glob('*.py')]

load_cogs_from_system(client, target_dir=".\cogs")

client.run(os.environ['BOT_TOKEN'])