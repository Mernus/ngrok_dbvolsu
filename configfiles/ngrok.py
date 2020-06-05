import requests
from log import set_log_settings
from pyngrok import ngrok
from settings import UPDATE_URL, NGROK_TOKEN

set_log_settings()
ngrok.set_auth_token(NGROK_TOKEN)

url = ngrok.connect(5432, "tcp")
ngrok_process = ngrok.get_ngrok_process()

try:
    parsed_url = url[6:].split(':')
    ngrok_host, ngrok_port = parsed_url
    post_data = {'host': ngrok_host, 'port': ngrok_port}

    r = requests.post(UPDATE_URL, data=post_data)
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print("~~~Shutting down server~~~")
    ngrok.kill()
