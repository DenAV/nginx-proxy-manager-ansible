# nginx-proxy-manager-ansible
a simple way to add a new proxy host via ansible playbook

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
        type: int
    ssl_forced:
        description: Is SSL Forced?
        required: false
        type: bool
    state:
        description: Whether to create (present), or remove (absent) a proxy host.
        required: false
        type: str
        choices=['absent', 'present']
