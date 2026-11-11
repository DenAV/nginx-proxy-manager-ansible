"""Regression tests for token conditionals using real Ansible execution."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def api():
    class Handler(BaseHTTPRequestHandler):
        hosts = []
        health_status = 200
        token_status = 200
        token_response = {"token": "test-token"}

        def log_message(self, *args):
            pass

        def respond(self, status, value):
            body = json.dumps(value).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            self.respond(self.health_status if self.path == "/api" else 200,
                         {"status": "ok"} if self.path == "/api" else self.hosts)

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path == "/api/tokens":
                self.respond(self.token_status, self.token_response)
            else:
                payload.update(id=len(self.hosts) + 1, certificate_id=0)
                self.hosts.append(payload)
                self.respond(201, payload)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/api", Handler
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.parametrize("mode", ["single", "batch", "batch_ssl"])
@pytest.mark.parametrize("scenario", ["success", "missing", "empty", "invalid_type", "rejected", "health_unauthorized"])
def test_role_token_handling(api, tmp_path, mode, scenario):
    executable = shutil.which("ansible-playbook")
    if executable is None:
        pytest.skip("ansible-playbook is required")
    url, handler = api
    if scenario == "missing":
        handler.token_response = {}
    elif scenario == "empty":
        handler.token_response = {"token": ""}
    elif scenario == "invalid_type":
        handler.token_response = {"token": 123}
    elif scenario == "rejected":
        handler.token_status = 401
    elif scenario == "health_unauthorized":
        handler.health_status = 401
    if mode == "single":
        role_vars = {"npm_api_domain_name": "test.example.com", "npm_api_host": "backend"}
    else:
        role_vars = {"npm_api_hosts": [{
            "domain_name": "test.example.com", "host": "backend", "ssl_forced": mode == "batch_ssl",
        }]}
    playbook = tmp_path / "play.yml"
    playbook.write_text(yaml.safe_dump([{
        "hosts": "localhost", "connection": "local", "gather_facts": False,
        "roles": [{"role": "npm-management", **role_vars}],
    }]))
    variables = tmp_path / "vars.json"
    variables.write_text(json.dumps({
        "npm_api_url": url, "npm_user": "test-user", "npm_password": "test-password",
        "ansible_python_interpreter": sys.executable,
    }))
    env = {
        **os.environ, "ANSIBLE_ROLES_PATH": str(ROOT / "roles"), "ANSIBLE_LIBRARY": str(ROOT / "library"),
        "ANSIBLE_LOCAL_TEMP": str(tmp_path / "ansible-tmp"), "ANSIBLE_NOCOLOR": "1", "ANSIBLE_NOCOWS": "1",
    }
    result = subprocess.run(
        [executable, "-i", "localhost,", str(playbook), "--extra-vars", "@" + str(variables)],
        cwd=tmp_path, env=env, text=True, capture_output=True, timeout=45, check=False,
    )
    assert "test-password" not in result.stdout + result.stderr
    assert "test-token" not in result.stdout + result.stderr
    if scenario == "success":
        assert result.returncode == 0, result.stdout + result.stderr
        assert len(handler.hosts) == 1
        assert handler.hosts[0]["domain_names"] == ["test.example.com"]
        assert handler.hosts[0].get("ssl_forced", False) is (mode == "batch_ssl")
    else:
        assert result.returncode != 0, result.stdout + result.stderr
        assert not handler.hosts
        if scenario != "rejected":
            assert "NPM authentication did not return a valid access token" in result.stdout + result.stderr
