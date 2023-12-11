#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, DenAV https://github.com/DenAV
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: nginx-proxy-manager-ansible

short_description: a simple way to add a new proxy host via ansible playbook

version_added: "1.0.0"

description: a simple way to add a new proxy host or to delete via ansible playbook

options:
    url:
        description: IP for the Nginx Proxy Manager REST API
        required: true
        type: str
    token:
        description: Tokens are required to authenticate against the API
        required: true
        type: str
    domain:
        description: Domain Names
        required: true
        type: str
    host:
        description: Forward Hostname / IP
        required: true
        type: str
    host_port:
        description: Forward Port 
        required: false
        default: 80
        type: int
    ssl_forced:
        description: Is SSL Forced?
        required: false
        default: true
        type: bool
    state:
        description: Whether to create (present), or remove (absent) a proxy host.
        required: false
        type: str
        choices=['absent', 'present']
'''
EXAMPLES = r'''
# create new proxy host
- name: Create Proxy-Host an NPM
  npm_proxy:
    url: "http://192.168.0.1:81/api"
    token: "npm_access_token"
    domain: "domain_name.example.com"
    host: "172.32.0.1"
    ssl_forced: True
    state: present

# delete proxy host
- name: Create Proxy-Host an NPM
  npm_proxy:
    url: "http://192.168.0.1:81/api"
    token: "npm_access_token"
    domain: "domain_name.example.com"
    host: "172.32.0.1"
    state: absent
'''
RETURN = r'''
# The return information.
msg:
  description: The output message that the nginx-proxy-manager-ansible module generates.
  returned: always
  type: str
  sample: "domain_name.example.com"
'''

# Install the Python Requests library:
# `pip install requests`

import requests
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def build_url(api_url, action, item_id=None):
    if action == "create-host":
        return "%s/nginx/proxy-hosts" % api_url, "POST"
    elif action == "search-host":
        return "%s/nginx/proxy-hosts" % api_url, "GET"
    elif action == "delete-host":
        return  "%s/nginx/proxy-hosts/%s" % (api_url, item_id), "DELETE"
    elif action == "create-ssl":
        return "%s/nginx/certificates" % api_url, "POST"
    elif action == "search-ssl":
        return "%s/nginx/certificates" % api_url, "GET"
    elif action == "delete-ssl":
        return  "%s/nginx/certificates/%s" % (api_url, item_id), "DELETE"

def http_request(api_url, token, action, data=None, item_id=None):
    
    if item_id is None:
        url, method = build_url(api_url, action)
    else:
        url, method = build_url(api_url, action, item_id)
    
    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    if method == "GET":
        response =  requests.get(url=url, data=data, headers=headers)
    elif method == "POST":
        response =  requests.post(url=url, data=data, headers=headers)
    elif method == "DELETE":
        response =  requests.delete(url=url, data=data, headers=headers)

    return response, response.status_code

def search_proxy_host(module, api_url, token, domain_name):
    response, info = http_request(api_url, token, action="search-host")
    
    status_code = info
    if status_code >= 400:
        module.fail_json("Failed to connect to api host to search for proxy_host. Info: %s" % response)

    result_search = ""
    for search in json.loads(response.text):
        if domain_name in search["domain_names"]:
            result_search = search
    
    # Return proxy_host
    return result_search

def create_proxy_host(module, api_url, token, domain_name, forward_host, forward_port, ssl_forced):
    # Create Proxy-host
    
    proxy_host = search_proxy_host(module, api_url, token, domain_name)

    if len(proxy_host) > 0:
        # If the Proxy-host already exists, do nothing
        return 0, "Proxy Host %s already exists" % domain_name
        
    else:
        forward_scheme = "http"

        if ssl_forced:
            data_request = json.dumps({
                "domain_names": [domain_name],
                "forward_host": forward_host,
                "forward_port": forward_port,
                "forward_scheme": forward_scheme,
                "certificate_id": "new",
                "ssl_forced": ssl_forced,
                "allow_websocket_upgrade": True,
            })
        else:
            data_request = json.dumps({
                "domain_names": [domain_name],
                "forward_host": forward_host,
                "forward_port": forward_port,
                "forward_scheme": forward_scheme,
            })

        response, info = http_request(api_url, token, data=data_request, action="create-host")

        status_code = info
        if status_code == 201:
            return 1, "Proxy-host %s created" % domain_name

        elif status_code >= 400:
            return 2, "Failed to connect to api host to create for proxy_host. Info: %s" % response

def delete_proxy_host(module, api_url, token, domain_name):
    # Delete Proxy-host
   
    proxy_host = search_proxy_host(module, api_url, token, domain_name)

    if len(proxy_host) > 0:
        # If the Proxy-host already exists, do remove
        if proxy_host['certificate_id'] > 0:
            # IF the Proxy-host have certificate
            rc, result = delete_certificate(module, api_url, token, item_id=proxy_host['certificate_id'])
            
            if rc == 0 or rc == 1:
                response, status_code = http_request(api_url, token, item_id=proxy_host['id'], action="delete-host")

                if status_code == 200:
                    return 1, "Proxy-host and certificate: %s remowed." % domain_name

                elif status_code >= 400:
                    return 2, "Failed to delete for Proxy-host and certificate: %s. Info: %s" % (domain_name, response)
            else:
                return 2, "Failed to delete for Proxy-host and certificate: %s. Info: %s" % (domain_name, result)

        else:
            response, status_code = http_request(api_url, token, item_id=proxy_host['id'], action="delete-host")

            if status_code == 200:
                return 1, "Proxy-host: %s remowed." % domain_name

            elif status_code >= 400:
                return 2, "Failed to delete for Proxy-host: %s. Info: %s" % (domain_name, response)

    else:
        return 0, "Proxy-host " + domain_name + " already deleted."

def search_certificate(module, api_url, token, domain_name=None, item_id=None):
    response, info = http_request(api_url, token, action="search-ssl")
    
    status_code = info
    if status_code >= 400:
        module.fail_json("Failed to search for certificate. Info: %s" % response)

    result_search = ""
    if domain_name is not None:
        for search in json.loads(response.text):
            if domain_name in search["domain_names"]:
                result_search = search
        
    elif item_id is not None:
        for search in json.loads(response.text):
            if item_id == search["id"]:
                result_search = search

    # Return certificate
    return result_search

def delete_certificate(module, api_url, token, item_id):
    
    certificate = search_certificate(module, api_url, token, item_id=item_id)

    if len(certificate) > 0:
        # If the certificate already exists, do remove
        response, info = http_request(api_url, token, item_id=item_id, action="delete-ssl")
        
        status_code = info
        if status_code == 200:
            result = "Certificate id: %s remowed" % item_id
            return 1, result

        elif status_code >= 400:
            result = "Failed to delete for certificate id: %s. Info: %s" % (item_id, response)
            return 2, result

    else:
        result = "Certificate id: %s does not exist." % item_id
        return 0, result

def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type='str', required=True),
            token=dict(type='str', required=True, no_log=True),
            domain=dict(type='str', required=True),
            host=dict(type='str', required=True),
            host_port=dict(type='int', required=False, default=80),
            ssl_forced=dict(type='bool', required=False, default=True),
            state=dict(type='str', default='present', choices=['absent', 'present']),
        ),
    )

    api_url = module.params['url']
    token = module.params['token']
    domain_name = module.params['domain']
    forward_host = module.params['host']
    forward_port = module.params['host_port']
    ssl_forced = module.params['ssl_forced']
    state = module.params['state']

    if state == 'present':
        (rc, result) = create_proxy_host(module, api_url, token, domain_name, forward_host, forward_port, ssl_forced)
    elif state == 'absent':
        (rc, result) = delete_proxy_host(module, api_url, token, domain_name)

    if rc == 2:
        module.fail_json(msg=result)
    elif rc == 1:
        module.exit_json(msg=result, changed=True)
    else:
        module.exit_json(msg=result, changed=False)

if __name__ == '__main__':
    main()
