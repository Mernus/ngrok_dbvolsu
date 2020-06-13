import requests
from log import set_log_settings
from pyngrok import ngrok
from settings import UPDATE_URL, NGROK_TOKEN, NGROK_DOWN, API_URL, CLEAR_REDIS_URL

set_log_settings()
ngrok.set_auth_token(NGROK_TOKEN)

url = ngrok.connect(5432, "tcp")
ngrok_process = ngrok.get_ngrok_process()

try:
    parsed_url = url[6:].split(':')
    ngrok_host, ngrok_port = parsed_url
    post_data = {'host': ngrok_host, 'port': ngrok_port}

    r = requests.post(API_URL + UPDATE_URL, data=post_data, verify=False)
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print(NGROK_DOWN)
    requests.post(API_URL + CLEAR_REDIS_URL, verify=False)
    ngrok.kill()
