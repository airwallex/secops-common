#!/usr/bin/env python3

import requests
from secops_common.secrets import read_config
from secops_common.misc import serialize


def send_message(project_id, text):
    webhook_url = read_config(project_id, 'slack')['hook_url']
    response = requests.post(webhook_url,
                             data=serialize({'text': text}),
                             headers={'Content-Type': 'application/json'})

    if (response.status_code != 200):
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s' %
            (response.status_code, response.text))


def send_block_message(project_id, data):
    webhook_url = read_config(project_id, 'slack')['hook_url']
    response = requests.post(webhook_url,
                             data=serialize(data),
                             headers={'Content-Type': 'application/json'})

    if (response.status_code != 200):
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s' %
            (response.status_code, response.text))
