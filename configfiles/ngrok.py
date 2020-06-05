from log import set_log_settings
import requests

from pyngrok import ngrok

set_log_settings()
ngrok.set_auth_token("1co4FrKt6QbXd1V1Pf04xfKLqR4_7AsdkpmamHM1D23jJWhen")

url = ngrok.connect(5432, "tcp")
ngrok_process = ngrok.get_ngrok_process()

try:
    parsed_url = url[6:].split(':')
    host, port = parsed_url
    post_data = {'host': host, 'port': port}
    print(post_data)

    r = requests.post("https://dbvolsu.herokuapp.com/def_update/", data=post_data)
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print("~~~Shutting down server~~~")
    ngrok.kill()
