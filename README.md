## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to:

- Install Docker (CE or EE)
- Install Docker Compose
- Configure the Docker daemon's options
- Set up 1 or more users to run Docker without needing root access
- Configure a cron job to run Docker clean up commands

## Why would you want to use this role?

If you're like me, you probably love Docker. This role provides everything you
need to get going with a production ready Docker host.

By the way, if you don't know what Docker is, or are looking to become an expert
with it then check out
[Dive into Docker: The Complete Docker Course for Developers](https://diveintodocker.com/?utm_source=ansibledocker&utm_medium=github&utm_campaign=readmetop).

## Supported platforms

- Ubuntu 16.04 LTS (Xenial)
- Debian 8 (Jessie)
- Debian 9 (Stretch)

## Role variables

```
# Do you want to install Community Edition ('ce') or Enterprise Edition ('ee')?
docker_edition: "ce"

# Do you want to install Docker through the "stable" or "edge" channel?
# Stable gets updated every quarter and Edge gets updated every month.
docker_channel: "edge"

# What version of Docker do you want to install?
docker_version: "18.04.0"

# Optionally install a specific version of Docker Compose.
docker_install_docker_compose: True
docker_compose_version: "1.21.0"

# A list of users to be added to the Docker group. For example if you have a
# user of 'deploy', then you'll want to set docker_users: ['deploy'] here.
#
# Keep in mind this user needs to already exist, it will not be created here.
docker_users: []

# A list of cron tasks to run. By default it will do a system prune every week
# on Sunday at midnight. This will help keep your Docker hosts' disks under
# control. 
docker_cron_tasks:
  - job: docker system prune -f
    name: "Docker clean up"
    # This uses the standard crontab syntax. 
    schedule: ["0", "0", "*", "*", "0"]

# Docker daemon options as they would appear on the command line, such as:
# docker_daemon_options:
#   - "--dns 8.8.8.8"
docker_daemon_options: []

# The APT GPG key id used to sign the Docker package.
docker_apt_key: "9DC858229FC7DD38854AE2D88D81803C0EBFCD88"

# Address of the Docker repository.
docker_repository: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker_channel }}"

# Full APT package name.
# Note: Docker versions 17.04 to 18.03 do not have that extra ~3 in the middle. 
docker_apt_package_name: "{{ docker_version }}~{{ docker_edition }}~3-0~{{ ansible_distribution | lower }}"

# How long should the apt-cache last in seconds?
docker_apt_cache_time: 86400
```

## Example usage

For the sake of this example let's assume you have a group called **app** and
you have a typical `site.yml` file.

To use this role edit your `site.yml` file to look something like this:

```
---

- name: "Configure app server(s)"
  hosts: "app"
  become: True

  roles:
    - { role: "nickjj.docker", tags: "docker" }
```

Let's say you want to add a deploy user to the Docker group, you can do this by
opening or creating `group_vars/app.yml` which is located relative to your
`inventory` directory and then making it look like this:

```
---

docker_users: ["deploy"]
```

*If you're looking for an Ansible role to create users, then check out my
[user role](https://github.com/nickjj/ansible-user)*.

Now you would run `ansible-playbook -i inventory/hosts site.yml -t docker`.

## Installation

`$ ansible-galaxy install nickjj.docker`

## Ansible Galaxy

You can find it on the official
[Ansible Galaxy](https://galaxy.ansible.com/nickjj/docker/) if you want to
rate it.

## License

MIT
