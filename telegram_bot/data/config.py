from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SUPPORT_ADMIN = env.str("SUPPORT_ADMIN")
API_URL = env.str("API_URL")
REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")


