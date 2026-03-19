# -*- coding: utf-8 -*-
"""Unit tests for library/npm_proxy.py

These tests mock the `requests` library to validate module logic
without requiring a running NPM instance.

Note: Ansible's module_utils.basic imports Unix-only modules (grp, pwd),
so we mock them before importing npm_proxy to allow tests on Windows.
"""

import json
import sys
import os
import types
import pytest
import requests
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------------------------
# Mock Unix-only modules and Ansible internals before importing npm_proxy.
# This allows tests to run on Windows where grp/pwd are not available.
# ---------------------------------------------------------------------------
for mod_name in ('grp', 'pwd'):
    if mod_name not in sys.modules:
        sys.modules[mod_name] = types.ModuleType(mod_name)

# Mock AnsibleModule so we don't need a full Ansible installation
mock_basic = types.ModuleType('ansible.module_utils.basic')
mock_basic.AnsibleModule = MagicMock
mock_urls = types.ModuleType('ansible.module_utils.urls')
mock_urls.fetch_url = MagicMock

for mod_name, mod_obj in {
    'ansible': types.ModuleType('ansible'),
    'ansible.module_utils': types.ModuleType('ansible.module_utils'),
    'ansible.module_utils.basic': mock_basic,
    'ansible.module_utils.urls': mock_urls,
}.items():
    sys.modules.setdefault(mod_name, mod_obj)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'library'))
import npm_proxy  # noqa: E402


# ---------------------------------------------------------------------------
# build_url tests
# ---------------------------------------------------------------------------
class TestBuildUrl:
    """Validate URL construction for each action."""

    def test_create_host(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "create-host")
        assert url == "http://localhost:81/api/nginx/proxy-hosts"
        assert method == "POST"

    def test_search_host(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "search-host")
        assert url == "http://localhost:81/api/nginx/proxy-hosts"
        assert method == "GET"

    def test_delete_host(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "delete-host", item_id=42)
        assert url == "http://localhost:81/api/nginx/proxy-hosts/42"
        assert method == "DELETE"

    def test_create_ssl(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "create-ssl")
        assert url == "http://localhost:81/api/nginx/certificates"
        assert method == "POST"

    def test_search_ssl(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "search-ssl")
        assert url == "http://localhost:81/api/nginx/certificates"
        assert method == "GET"

    def test_delete_ssl(self):
        url, method = npm_proxy.build_url("http://localhost:81/api", "delete-ssl", item_id=7)
        assert url == "http://localhost:81/api/nginx/certificates/7"
        assert method == "DELETE"

    def test_unknown_action_raises_value_error(self):
        """Unknown action should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown action"):
            npm_proxy.build_url("http://localhost:81/api", "unknown-action")


# ---------------------------------------------------------------------------
# http_request tests
# ---------------------------------------------------------------------------
class TestHttpRequest:
    """Validate HTTP method dispatch."""

    @patch("npm_proxy.requests.get")
    def test_get_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response, status = npm_proxy.http_request(
            "http://localhost:81/api", "test-token", action="search-host"
        )
        assert status == 200
        mock_get.assert_called_once()

    @patch("npm_proxy.requests.post")
    def test_post_request(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        response, status = npm_proxy.http_request(
            "http://localhost:81/api", "test-token",
            action="create-host", data='{"test": true}'
        )
        assert status == 201
        mock_post.assert_called_once()

    @patch("npm_proxy.requests.delete")
    def test_delete_request(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        response, status = npm_proxy.http_request(
            "http://localhost:81/api", "test-token",
            action="delete-host", item_id=1
        )
        assert status == 200
        mock_delete.assert_called_once()

    @patch("npm_proxy.requests.get")
    def test_auth_header_is_set(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        npm_proxy.http_request(
            "http://localhost:81/api", "my-secret-token", action="search-host"
        )
        call_kwargs = mock_get.call_args
        headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers")
        assert headers["Authorization"] == "Bearer my-secret-token"
        assert headers["Content-Type"] == "application/json"

    @patch("npm_proxy.requests.get")
    def test_timeout_is_set(self, mock_get):
        """Verify default timeout=30 is passed to requests calls."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        npm_proxy.http_request(
            "http://localhost:81/api", "token", action="search-host"
        )
        call_kwargs = mock_get.call_args
        timeout = call_kwargs.kwargs.get("timeout") or call_kwargs[1].get("timeout")
        assert timeout == 30

    @patch("npm_proxy.requests.post")
    def test_timeout_ssl_is_120(self, mock_post):
        """Verify timeout=120 can be passed for SSL operations."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        npm_proxy.http_request(
            "http://localhost:81/api", "token", action="create-host",
            data="{}", timeout=120
        )
        call_kwargs = mock_post.call_args
        timeout = call_kwargs.kwargs.get("timeout") or call_kwargs[1].get("timeout")
        assert timeout == 120

    @patch("npm_proxy.requests.get")
    def test_connection_error_is_raised(self, mock_get):
        """ConnectionError from requests should propagate."""
        mock_get.side_effect = requests.exceptions.ConnectionError("refused")

        with pytest.raises(requests.exceptions.ConnectionError, match="Failed to connect"):
            npm_proxy.http_request(
                "http://localhost:81/api", "token", action="search-host"
            )

    @patch("npm_proxy.requests.post")
    def test_timeout_error_is_raised(self, mock_post):
        """Timeout from requests should propagate."""
        mock_post.side_effect = requests.exceptions.Timeout("timed out")

        with pytest.raises(requests.exceptions.Timeout, match="timed out"):
            npm_proxy.http_request(
                "http://localhost:81/api", "token",
                action="create-host", data='{"test": true}'
            )


# ---------------------------------------------------------------------------
# search_proxy_host tests
# ---------------------------------------------------------------------------
class TestSearchProxyHost:
    """Validate proxy host search logic."""

    @patch("npm_proxy.http_request")
    def test_found(self, mock_http):
        mock_response = MagicMock()
        mock_response.text = json.dumps([
            {"id": 1, "domain_names": ["site-a.example.com"]},
            {"id": 2, "domain_names": ["site-b.example.com"]},
        ])
        mock_http.return_value = (mock_response, 200)

        module = MagicMock()
        result = npm_proxy.search_proxy_host(
            module, "http://localhost:81/api", "token", "site-b.example.com"
        )
        assert result["id"] == 2

    @patch("npm_proxy.http_request")
    def test_not_found(self, mock_http):
        mock_response = MagicMock()
        mock_response.text = json.dumps([
            {"id": 1, "domain_names": ["site-a.example.com"]},
        ])
        mock_http.return_value = (mock_response, 200)

        module = MagicMock()
        result = npm_proxy.search_proxy_host(
            module, "http://localhost:81/api", "token", "nonexistent.example.com"
        )
        assert result is None


# ---------------------------------------------------------------------------
# create_proxy_host tests
# ---------------------------------------------------------------------------
class TestCreateProxyHost:
    """Validate proxy host creation logic."""

    @patch("npm_proxy.http_request")
    @patch("npm_proxy.search_proxy_host")
    def test_create_new_host(self, mock_search, mock_http):
        mock_search.return_value = None  # not found

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_http.return_value = (mock_response, 201)

        module = MagicMock()
        rc, msg = npm_proxy.create_proxy_host(
            module, "http://localhost:81/api", "token",
            "new-site.example.com", "10.0.0.1", 80, False, ''
        )
        assert rc == 1
        assert "created" in msg

    @patch("npm_proxy.search_proxy_host")
    def test_host_already_exists(self, mock_search):
        mock_search.return_value = {"id": 1, "domain_names": ["existing.example.com"]}

        module = MagicMock()
        rc, msg = npm_proxy.create_proxy_host(
            module, "http://localhost:81/api", "token",
            "existing.example.com", "10.0.0.1", 80, False, ''
        )
        assert rc == 0
        assert "already exists" in msg

    @patch("npm_proxy.http_request")
    @patch("npm_proxy.search_proxy_host")
    def test_create_with_ssl(self, mock_search, mock_http):
        mock_search.return_value = None  # not found

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_http.return_value = (mock_response, 201)

        module = MagicMock()
        rc, msg = npm_proxy.create_proxy_host(
            module, "http://localhost:81/api", "token",
            "ssl-site.example.com", "10.0.0.1", 443, True, ''
        )
        assert rc == 1

        # Verify SSL-related fields were sent
        call_args = mock_http.call_args
        data = json.loads(call_args.kwargs.get("data") or call_args[1].get("data"))
        assert data["ssl_forced"] is True
        assert data["certificate_id"] == "new"
        assert "meta" not in data

    @patch("npm_proxy.http_request")
    @patch("npm_proxy.search_proxy_host")
    def test_create_with_ssl_and_letsencrypt(self, mock_search, mock_http):
        mock_search.return_value = None  # not found

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_http.return_value = (mock_response, 201)

        module = MagicMock()
        rc, msg = npm_proxy.create_proxy_host(
            module, "http://localhost:81/api", "token",
            "le-site.example.com", "10.0.0.1", 443, True,
            "admin@example.com"
        )
        assert rc == 1

        # Verify meta with letsencrypt fields was sent
        call_args = mock_http.call_args
        data = json.loads(call_args.kwargs.get("data") or call_args[1].get("data"))
        assert data["ssl_forced"] is True
        assert data["certificate_id"] == "new"
        assert data["meta"]["letsencrypt_email"] == "admin@example.com"
        assert data["meta"]["letsencrypt_agree"] is True
        assert data["meta"]["dns_challenge"] is False

    @patch("npm_proxy.http_request")
    @patch("npm_proxy.search_proxy_host")
    def test_create_api_error(self, mock_search, mock_http):
        mock_search.return_value = None  # not found

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_http.return_value = (mock_response, 500)

        module = MagicMock()
        rc, msg = npm_proxy.create_proxy_host(
            module, "http://localhost:81/api", "token",
            "fail.example.com", "10.0.0.1", 80, False, ''
        )
        assert rc == 2
        assert "Failed" in msg


# ---------------------------------------------------------------------------
# delete_proxy_host tests
# ---------------------------------------------------------------------------
class TestDeleteProxyHost:
    """Validate proxy host deletion logic."""

    @patch("npm_proxy.http_request")
    @patch("npm_proxy.search_proxy_host")
    def test_delete_host_no_cert(self, mock_search, mock_http):
        mock_search.return_value = {"id": 5, "domain_names": ["del.example.com"], "certificate_id": 0}

        mock_response = MagicMock()
        mock_http.return_value = (mock_response, 200)

        module = MagicMock()
        rc, msg = npm_proxy.delete_proxy_host(
            module, "http://localhost:81/api", "token", "del.example.com"
        )
        assert rc == 1

    @patch("npm_proxy.search_proxy_host")
    def test_delete_nonexistent(self, mock_search):
        mock_search.return_value = None  # not found

        module = MagicMock()
        rc, msg = npm_proxy.delete_proxy_host(
            module, "http://localhost:81/api", "token", "gone.example.com"
        )
        assert rc == 0
        assert "already deleted" in msg
