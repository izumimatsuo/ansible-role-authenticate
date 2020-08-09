import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_create_group(host):
    assert host.group('maintainer').exists
    assert host.group('adminuser').exists


def test_sudoers(host):
    assert host.file('/etc/sudoers.d/adminuser').exists


def test_create_user(host):
    user = host.user('test')
    assert user.exists
    assert user.group.startswith('maintainer')
    assert 'maintainer' in user.groups
    assert 'adminuser' in user.groups


def test_ssh_public_key(host):
    assert host.file('/home/test/.ssh/authorized_keys').exists


def test_package(host):
    assert host.package('google-authenticator').is_installed
