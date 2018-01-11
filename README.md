## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to install Docker and
optionally Docker Compose.

##### Supported platforms

- Ubuntu 16.04 LTS (Xenial)
- Debian 8 (Jessie)
- Debian 9 (Stretch)

### What problem does it solve and why is it useful?

If you're like me, you probably love Docker. This role lets you install a specific
version of Docker as well as Docker Compose.

If you don't know what Docker is, or are looking to become an expert with it
then check out [Dive Into Docker: The Complete Docker Course for Developers](https://diveintodocker.com/courses/dive-into-docker?utm_source=ansibledocker&utm_medium=github&utm_campaign=readmetop).

## Role variables

Below is a list of default values along with a description of what they do.

```
---

# Do you want to install Community Edition ('ce') or Enterprise Edition ('ee')?
docker_edition: 'ce'

# Do you want to install Docker through the 'stable' or 'edge' channel?
# Stable gets updated every quarter and Edge gets updated every month.
docker_channel: 'edge'

# What version of Docker do you want to install?
docker_version: '17.12.0'

# Optionally install a specific version of Docker Compose.
docker_install_docker_compose: True
docker_compose_version: '1.18.0'

# A list of users to be added to the Docker group. For example if you have a
# user of 'deploy', then you'll want to set docker_users: ['deploy'] here.
#
# Keep in mind this user needs to already exist, it will not be created here.
docker_users: []

# A list of Docker options as they would appear on the command line, such as:
# docker_options:
#   - '--dns 8.8.8.8'
docker_options: []

# The APT GPG key id used to sign the Docker package.
docker_apt_key: '9DC858229FC7DD38854AE2D88D81803C0EBFCD88'

# The OS distribution and distribution release, thanks https://github.com/debops.
# Doing it this way doesn't depend on having lsb-release installed.
docker_distribution: '{{ ansible_local.core.distribution
                         if (ansible_local|d() and ansible_local.core|d() and
                             ansible_local.core.distribution|d())
                         else ansible_distribution }}'
docker_distribution_release: '{{ ansible_local.core.distribution_release
                                 if (ansible_local|d() and ansible_local.core|d() and
                                     ansible_local.core.distribution_release|d())
                                 else ansible_distribution_release }}'

# Address of the Docker repository.
docker_repository: 'deb [arch=amd64] https://download.docker.com/linux/{{ docker_distribution | lower }} {{ docker_distribution_release }} {{ docker_channel }}'

# How long should the apt-cache last in seconds?
docker_apt_cache_time: 86400
```

## Example playbook

For the sake of this example let's assume you have a group called **app** and
you have a typical `site.yml` file.

To use this role edit your `site.yml` file to look something like this:

```
---

- name: Configure app server(s)
  hosts: app
  become: True

  roles:
    - { role: nickjj.docker, tags: docker }
```

Let's say you want to add a deploy user to the Docker group, you can do this by
opening or creating `group_vars/app.yml` which is located relative to your
`inventory` directory and then making it look like this:

```
---

docker_users: ['deploy']
```

If you're looking for an Ansible role to create users, then check out my
[user role](https://github.com/nickjj/ansible-user).

## Installation

`$ ansible-galaxy install nickjj.docker`

## Ansible Galaxy

You can find it on the official
[Ansible Galaxy](https://galaxy.ansible.com/nickjj/docker/) if you want to
rate it.

## License

MIT
