import dotenv
import logging
import multiprocessing
import os
import pyrogram
import time

logging.basicConfig(format="[%(levelname)s] %(message)s")

# Checking of .env file
if os.path.exists(".env"):
    dotenv.load_dotenv(".env")
else:
    logging.warning("[Init] Couldn't find .env file, using system environment instead!")

env = os.environ
api_id = env.get("API_ID", None)
api_hash = env.get("API_HASH", None)
bot_token = env.get("BOT_TOKEN", None)
owner = env.get("OWNER_ID", None)
debug = str(env.get("DEBUG", None)).lower()
cpu_count = multiprocessing.cpu_count()
start_time = time.time()

if not api_id or not api_hash or not bot_token:
    logging.error("[init] API_ID, API_HASH or BOT_TOKEN not found. Aborting.")
    raise ValueError("Environment is missing!")

if bot_token == "" or bot_token is None:
    raise ValueError("Bot Token cannot be empty or None.")

if debug in ['true', 'on', 'yes']:
    debug = True
else:
    debug = False

try:
    api_id = int(api_id)
    owner = int(owner)
except TypeError as e:
    raise TypeError("Environment is missing or value is wrong!")

client = pyrogram.Client("bot_session", api_id, api_hash, in_memory=True, workers=cpu_count * 4, bot_token=bot_token)

with client:
    me = client.get_me()