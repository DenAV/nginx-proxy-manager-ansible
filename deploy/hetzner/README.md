# Hetzner Cloud deployment

Hetzner Cloud CX22 uses the project's Docker Compose file directly.
See the [Deployment Guide](https://github.com/DenAV/nginx-proxy-manager-ansible/wiki/Deployment-Guide#option-1-hetzner-cloud-cx22--docker-ce) for full instructions.

## Files

| File | Description |
|------|-------------|
| `cloud-config.yml` | Cloud-init config for initial server hardening (SSH, UFW, fail2ban) |

## Cloud-config

Automates server hardening on first boot: creates `deploy` user, sets SSH to port 2222, disables root login, enables UFW and fail2ban.

**Usage (Hetzner UI):** Paste contents of `cloud-config.yml` into the **Cloud config** field when creating a server.

**Usage (CLI):**

```bash
hcloud server create \
  --name npm-server \
  --type cx22 \
  --image docker-ce \
  --ssh-key my-key \
  --location nbg1 \
  --user-data-from-file deploy/hetzner/cloud-config.yml
```

> Replace `<your-public-ssh-key>` in `cloud-config.yml` with your actual SSH public key before use.

## Quick start

```bash
ssh deploy@<server-ip> -p 2222
git clone https://github.com/DenAV/nginx-proxy-manager-ansible.git /opt/npm
cd /opt/npm/docker
cp .env.example .env
docker compose -f docker-compose_npm.yml up -d
```
