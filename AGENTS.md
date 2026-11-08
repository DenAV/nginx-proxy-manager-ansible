# Nginx Proxy Manager Ansible

## Repository boundaries

- `../nginx-proxy-manager-ansible.wiki/` is a separate Git checkout for the GitHub wiki. Consult relevant pages for documentation changes; its commits and pushes are independent of this repository.
- The ignored `_ToDo/ToDo.md` holds the local review backlog and agreed priorities. Keep it local; historical checkboxes are not current verification evidence.

## Git workflow

- This is a multi-branch project: `feature/*` or `fix/*` -> `develop` -> `main`. Base implementation branches on `develop` and target PRs to `develop`; promote reviewed changes from `develop` to `main`. Do not implement directly on `main`.
- Obtain approval before creating branches, committing, pushing, opening PRs, or merging. Do not switch branches while existing changes could be lost or carried into the wrong branch; preserve the current work and resolve the branch choice first.

## Execution flow

- `pl_npm-management.yml` invokes `roles/npm-management/`: credentials -> health check -> token -> single-host or batch `npm_proxy` calls, delegated to localhost.
- `library/npm_proxy.py` is a standalone Ansible module using `requests`, not an installed Python package or Ansible Collection. Runtime dependencies must be available to the Python interpreter executing the delegated module.
- When adding module options, check `argument_spec`, `DOCUMENTATION`/examples, role defaults, and all three role invocation tasks (single, non-SSL batch, SSL batch). Batch fields use item keys, while single-host fields use `npm_api_*` variables.
- Module `ssl_forced` defaults to `true`, but the role defaults it to `false`. Do not assume direct module calls and role calls have identical defaults.

## Local verification

Run from the repository root with an activated virtual environment. CI uses Python 3.11; install development tools with `python -m pip install -r requirements-dev.txt`.

```sh
make lint
ANSIBLE_ROLES_PATH=./roles ANSIBLE_LIBRARY=./library make syntax
python -m pytest tests/ -v --tb=short
python -m pytest tests/test_npm_proxy.py::TestCreateProxyHost::test_create_new_host -q
python -m pytest tests/ --cov=library --cov-report=term
```

- Unit tests insert `library/` into `sys.path` and mock Ansible internals and HTTP calls. They need no running NPM, but do not prove real Ansible argument handling or role execution.
- `make pre-commit` needs `pre-commit` installed separately; it is not in `requirements-dev.txt`. Its Ansible hook excludes `molecule/`, `docker/`, `deploy/`, and `docs/`, unlike CI's `ansible-lint .`.
- `.flake8` permits imports after Ansible documentation blocks (`E402`) in `library/*.py`; preserve this layout.
- `.github/workflows/ci.yml` is the executable CI source: lint, syntax, unit tests; pushes to `main`/`develop`, PRs to `develop` only. There is no integration workflow despite README/wiki claims.
- `molecule test` is opt-in integration work requiring Docker. The current scenario starts privileged NPM, binds ports 3080/3081/3443 and 8080 on all interfaces, and reuses fixed host directories for data/certificates. Inspect its isolation before running; it is not a harmless unit check.

## Operational pitfalls

- Do not run the example playbook as verification: it creates an SSL host and may request a real Let's Encrypt certificate. Use `--syntax-check` for static validation.
- Current `state: present` is create-only: existing domains are returned unchanged even when backend/SSL settings differ. Current `state: absent` deletes the entire matching multi-domain host and deletes its certificate first, without checking other users of that certificate. Do not exercise deletion against shared/live data.
- The module does not yet advertise Ansible check-mode support; do not describe `--check` as a working preview.
- Credentials normally come from the ignored `roles/npm-management/vars/api_secret.yml` (Vault). The role currently scans the whole vars directory without excluding `api_secret.example`; renaming the example alone did not fix loading.
- Inspect transport before live API work: token acquisition currently disables TLS certificate validation. Treat this as a known defect, not a pattern to copy.
