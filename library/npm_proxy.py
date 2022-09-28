#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
__metaclass__ = type

#
#
#

# Install the Python Requests library:
# `pip install requests`

import requests
import json

from ansible.module_utils.basic import AnsibleModule


def create_proxy_host(module, url, token, domain_name, forward_host, forward_port):
    # Create Proxy-host
    # "/nginx/proxy-hosts"

    forward_scheme = "http"

    try:
        response = requests.post(
            url = url + "/nginx/proxy-hosts",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                "X-API-Version": "next"
            },
            data=json.dumps({
                "domain_names": [domain_name],
                "forward_host": forward_host,
                "forward_port": forward_port,
                "forward_scheme": forward_scheme,
                "certificate_id": "new",
                "ssl_forced": True,
                "allow_websocket_upgrade": True,
            })
        )
        if response.status_code == 201:
            module.exit_json(changed=True, msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
        elif response.status_code == 400:
            module.fail_json(msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
        elif response.status_code == 500:
            module.fail_json(msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))            
        else:
            module.exit_json(changed=False, msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))

    except requests.exceptions.RequestException:
        module.fail_json(changed=False, msg='You HTTP requested this to fail')

def create_certificates(module, url, token, domain_name):
    # Creates a new Certificate
    # "/nginx/certificates"
    try:
        response = requests.post(
            url = url + "/nginx/certificates",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
            },
            data=json.dumps({
                "domain_names": [domain_name],
                "provider": "letsencrypt",
            })
        )

        if response.status_code == 201:
            module.exit_json(changed=True, msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
        elif response.status_code == 400:
            module.fail_json(msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
        elif response.status_code == 500:
            module.fail_json(msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
        else:
            module.exit_json(changed=False, msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))
#         return change, ssl_id

    except requests.exceptions.RequestException:
        module.fail_json(msg='You HTTP requested this to fail')

def get_certificates(module, url, token):
    # Creates a new Certificate
    # "/nginx/certificates"
    try:
        response = requests.get(
            url = url + "/nginx/certificates",
            headers={
                "Authorization": "Bearer " + token,
            },
        )

        module.exit_json(changed=False, msg="Status Code: %s ,Response Body: %s" % (response.status_code, response.content ))

    except requests.exceptions.RequestException:
        module.fail_json(msg='You HTTP requested this to fail')



def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type='str', required=True),
            token=dict(type='str', required=True),
            domain=dict(type='str', required=True),
            host=dict(type='str', required=True),
            host_port=dict(type='int', required=False, default=80),
            ssl_forced=dict(type='bool', required=False, default=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
        ),
    )

    url = module.params['url']
    token = module.params['token']
    domain_name = module.params['domain']
    forward_host = module.params['host']
    forward_port = module.params['host_port']
    ssl_forced = module.params['ssl_forced']
    state = module.params['state']

#    if ssl_forced:
#  check, before, after = svn.needs_update()
#       create_certificates(module, url, token, domain_name)
#    get_certificates(module, url, token)
    create_proxy_host(module, url, token, domain_name, forward_host, forward_port)

if __name__ == '__main__':
    main()
