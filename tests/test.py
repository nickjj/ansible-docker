import re


def test_docker_version(host):
    assert 0 == host.run("docker --version").rc


def test_pinned_docker_version(host):
    existing_docker_version = host.check_output("docker --version")
    host.run("sudo apt-get update")
    host.run("sudo apt-get upgrade")
    docker_version_after_apt_update = host.check_output("docker --version")

    assert existing_docker_version == docker_version_after_apt_update


def test_able_to_access_docker_without_root(host):
    assert "docker" in host.user("test").groups


def test_daemon_json_is_configured(host):
    daemon_json = host.file("/etc/docker/daemon.json")

    assert daemon_json.contains("journald")
    assert daemon_json.contains("8.8.8.8")


def test_customized_environment_systemd_unit_file(host):
    unit_file = "/etc/systemd/system/docker.service.d/environment.conf"
    file_contents = host.file(unit_file).content_string

    assert re.search(r"Environment=\"HTTP_PROXY=.*\"", file_contents)
    assert re.search(r"Environment=\"HTTPS_PROXY=.*\"", file_contents)


def test_customized_daemon_flags_systemd_unit_file(host):
    unit_file = "/etc/systemd/system/docker.service.d/options.conf"
    file_contents = host.file(unit_file).content_string

    assert "-H fd://" in file_contents
    assert "--debug" in file_contents


def test_customized_systemd_override(host):
    unit_file = "/etc/systemd/system/docker.service.d/custom.conf"
    file_contents = host.file(unit_file).content_string

    assert "ATest" in file_contents


def test_docker_compose_is_pip_installed_and_symlinked(host):
    assert 0 == host.run("docker-compose --version").rc


def test_python_docker_is_symlinked(host):
    assert 0 == host.run("python-docker --version").rc


def test_docker_clean_up_cron_job(host):
    cron_conf = host.file("/etc/cron.d/docker-disk-clean-up").content_string

    assert "test docker system prune -af" in cron_conf


def test_python_docker_module(host):
    assert 0 == host.run("python-docker -c 'import docker'").rc
