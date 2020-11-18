import logging
import requests
import sys

import settings

from pyngrok import ngrok, conf
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import signal


def signal_handler():
    print("Keybord")


signal.signal(signal.SIGTERM, signal_handler)


class NgrokServer:
    __working = False
    __active_tunnel = None

    def __new__(cls):
        if cls.__working:
            return

        cls.__init_settings()

        cls.__active_tunnel = ngrok.connect(5432, "tcp")
        ngrok_process = ngrok.get_ngrok_process()

        if not ngrok_process.healthy():
            print("\n\033[31m[ERROR]: Ngrok server has some error\033[0m")
            # print("\n\033[31m[ERROR]: Error log can be find: \033[0m")
            print(settings.NGROK_DOWN_STR)

            ngrok.kill()
        else:
            cls.__working = True

        return super(NgrokServer, cls).__new__(cls)

    def __init__(self):
        if not self.__working:
            return None

        ngrok_host, ngrok_port = self.__active_tunnel.public_url[6:].split(':')
        post_data = {'host': ngrok_host, 'port': ngrok_port}

        requests.post(settings.API_URL + settings.UPDATE_URL, data=post_data, verify=False)

        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()

    def kill(self):
        if not self.__working:
            return False

        self.__kill_proc()

        self.__working = None
        self.__active_tunnel = None

        return True

    @staticmethod
    def __kill_proc():
        print(settings.NGROK_DOWN_STR)

        requests.post(settings.API_URL + settings.CLEAR_REDIS_URL, verify=False)
        ngrok.kill()

    @property
    def is_working(self):
        return self.__working

    @property
    def get_tunnel(self):
        return self.__active_tunnel if self.__working else None

    @staticmethod
    def __log_setup():
        log_level = settings.LOG_LEVEL

        logger = logging.getLogger()
        logger.setLevel(log_level)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(log_level)

        formatter = logging.Formatter(settings.LOG_FORMAT)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    @classmethod
    def __init_settings(cls):
        cls.__log_setup()

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        ngrok_params = {
            "auth_token": settings.NGROK_DEFAULT_TOKEN,
            "max_logs": settings.NGROK_DEFAULT_MAX_LOGS,
            "request_timeout": settings.NGROK_TIMEOUT
        }

        pyngrok_cfg = conf.PyngrokConfig(**ngrok_params)
        conf.set_default(pyngrok_config=pyngrok_cfg)
