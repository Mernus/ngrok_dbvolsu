import logging
import sys

from pyngrok import ngrok

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

ngrok.set_auth_token("1co4FrKt6QbXd1V1Pf04xfKLqR4_7AsdkpmamHM1D23jJWhen")
url = ngrok.connect(5432, "tcp")
ngrok_process = ngrok.get_ngrok_process()

try:
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print(" Shutting down server.")
    ngrok.kill()
