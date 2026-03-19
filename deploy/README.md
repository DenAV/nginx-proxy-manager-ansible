# Deployment

Cloud deployment manifests for Nginx Proxy Manager.

For full step-by-step instructions, see the [Deployment Guide](https://github.com/DenAV/nginx-proxy-manager-ansible/wiki/Deployment-Guide) wiki page.

## Providers

| Directory | Provider | Description |
|-----------|----------|-------------|
| [azure/](azure/) | Azure Container Instances | ACI deployment manifest with Azure File Share volumes |
| [hetzner/](hetzner/) | Hetzner Cloud | CX22 VM + Docker CE (uses `docker/docker-compose_npm.yml`) |

## Quick start

**Azure ACI:**

```bash
# Edit placeholders in the manifest
cp deploy/azure/npm-aci.yaml npm-aci.yaml
# Replace <storage-account> and <storage-key> with your values
az container create --resource-group <rg> --file npm-aci.yaml
```

**Hetzner Cloud:**

```bash
ssh root@<server-ip>
git clone https://github.com/DenAV/nginx-proxy-manager-ansible.git /opt/npm
cd /opt/npm/docker
docker compose -f docker-compose_npm.yml up -d
```
