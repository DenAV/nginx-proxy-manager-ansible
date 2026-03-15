# Hetzner Cloud deployment

Hetzner Cloud CX22 uses the project's Docker Compose file directly.
No provider-specific manifest is needed — see the [Deployment Guide](https://github.com/DenAV/nginx-proxy-manager-ansible/wiki/Deployment-Guide#option-1-hetzner-cloud-cx22--docker-ce) for full instructions.

## Quick start

```bash
ssh root@<server-ip>
git clone https://github.com/DenAV/nginx-proxy-manager-ansible.git /opt/npm
cd /opt/npm/docker
cp .env.example .env
docker compose -f docker-compose_npm.yml up -d
```
