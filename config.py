from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("token")
id_of_main_channel = int(os.getenv("id_of_main_channel"))
link_to_bot = os.getenv("link_to_bot")