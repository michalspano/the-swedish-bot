from os import getenv
from dotenv import load_dotenv
from tweepy import OAuthHandler, API

def export_API() -> API | None:
    load_dotenv() # Load .env file

    auth: OAuthHandler = OAuthHandler(
        getenv("API_KEY"), getenv("API_SECRET_KEY"))
    auth.set_access_token(getenv("ACCESS_TOKEN"),
                          getenv("ACCESS_TOKEN_SECRET"))
    api: API = API(auth, wait_on_rate_limit=True)
    if not api.verify_credentials():
        raise Exception("Authentication failed")
    return api
