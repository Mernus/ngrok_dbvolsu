import logging

# Log setting
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Params for api
# SERVER_HOST = "https://dbvolsu.herokuapp.com/"
SERVER_HOST = "http://127.0.0.1:8000/"
API_URL = SERVER_HOST + "api/"
UPDATE_URL = "def_update/"
CLEAR_REDIS_URL = "redis_clear/"

# Ngrok parameters
NGROK_DEFAULT_TOKEN = "1co4FrKt6QbXd1V1Pf04xfKLqR4_7AsdkpmamHM1D23jJWhen"
NGROK_DEFAULT_MAX_LOGS = 10
NGROK_TIMEOUT = 2
NGROK_DOWN_STR = '@' * 34 + "\n@@@    SHUTTING DOWN SERVER    @@@\n" + '@' * 34
