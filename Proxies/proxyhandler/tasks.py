from celery import shared_task

import time
import requests
from celery_progress.backend import ProgressRecorder

WEBSITE_URL = "http://127.0.0.1:8000"


@shared_task
def verification_request():
    try:
        requests.get(WEBSITE_URL + "/verify")
        return 1
    except requests.RequestException as exc:
        return -1


@shared_task
def verification_request():
    try:
        requests.get(WEBSITE_URL + "/scrap")
        return 1
    except requests.RequestException as exc:
        return -1
