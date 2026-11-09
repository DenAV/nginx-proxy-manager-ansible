"""Run the role's credential-loading tasks without contacting the NPM API."""

import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml


ROLE = Path(__file__).resolve().parents[1] / 'roles' / 'npm-management'
CREDENTIALS = {'npm_user': 'test-user', 'npm_password': 'test-password'}


@pytest.fixture
def run_role(tmp_path):
    executable = shutil.which('ansible-playbook')
    if executable is None:
        pytest.skip('ansible-playbook is required for role variable-loading tests')

    role = tmp_path / 'roles' / 'npm-management'
    (role / 'tasks').mkdir(parents=True)
    (role / 'vars').mkdir()
    tasks = yaml.safe_load((ROLE / 'tasks' / 'main.yml').read_text())[:2]
    for task in tasks:
        assert any(key in task for key in (
            'include_vars', 'ansible.builtin.include_vars', 'assert', 'ansible.builtin.assert',
        ))
    (role / 'tasks' / 'main.yml').write_text(yaml.safe_dump(tasks))
    for name in ('main.yml', 'api_secret.example'):
        shutil.copyfile(ROLE / 'vars' / name, role / 'vars' / name)

    config = tmp_path / 'ansible.cfg'
    config.write_text('[defaults]\nretry_files_enabled = False\n')
    playbook = tmp_path / 'playbook.yml'
    playbook.write_text(yaml.safe_dump([{
        'name': 'Test NPM credential loading',
        'hosts': 'localhost',
        'gather_facts': False,
        'roles': ['npm-management'],
        'tasks': [{
            'name': 'Verify supplied credentials were preserved',
            'ansible.builtin.assert': {'that': [
                "npm_user == 'test-user'",
                "npm_password == 'test-password'",
            ]},
            'no_log': True,
        }],
    }]))
    env = {
        **os.environ,
        'ANSIBLE_CONFIG': str(config),
        'ANSIBLE_LOCAL_TEMP': str(tmp_path / 'ansible-tmp'),
        'ANSIBLE_ROLES_PATH': str(tmp_path / 'roles'),
        'ANSIBLE_NOCOLOR': '1',
        'ANSIBLE_NOCOWS': '1',
    }

    def run(credentials=None, vault=False):
        inventory = tmp_path / 'inventory.yml'
        host_vars = {'ansible_connection': 'local'}
        args = [executable, '-i', str(inventory), str(playbook)]
        if vault:
            secrets = role / 'vars' / 'api_secret.yml'
            secrets.write_text(yaml.safe_dump(credentials))
            password_file = tmp_path / 'vault-password'
            password_file.write_text('test-only-vault-password\n')
            vault_executable = str(Path(executable).with_name('ansible-vault'))
            subprocess.run(
                [vault_executable, 'encrypt', '--vault-password-file', str(password_file), str(secrets)],
                env=env, cwd=tmp_path, capture_output=True, text=True, check=True, timeout=30,
            )
            args.extend(['--vault-password-file', str(password_file)])
        elif credentials is not None:
            host_vars.update(credentials)
        inventory.write_text(yaml.safe_dump({'all': {'hosts': {'localhost': host_vars}}}))
        return subprocess.run(args, env=env, cwd=tmp_path, capture_output=True, text=True, timeout=30)

    return run


@pytest.mark.parametrize('vault', [False, True], ids=['inventory', 'vault'])
def test_credentials_load_with_example_present(run_role, vault):
    result = run_role(CREDENTIALS, vault=vault)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert CREDENTIALS['npm_password'] not in output


@pytest.mark.parametrize('credentials', [
    None,
    {'npm_password': 'test-password'},
    {'npm_user': 'test-user', 'npm_password': ''},
], ids=['missing', 'missing-user', 'empty-password'])
def test_invalid_credentials_fail_with_actionable_error(run_role, credentials):
    result = run_role(credentials)
    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert 'NPM API credentials (npm_user/npm_password) are missing or empty.' in output
    assert 'api_secret.yml' in output
    assert CREDENTIALS['npm_password'] not in output
