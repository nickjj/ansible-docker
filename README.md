## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to install Docker and
Docker Compose.

##### Supported platforms:

- Ubuntu 16.04 LTS (Xenial)
- Debian 8 (Jessie)

### What problem does it solve and why is it useful?

If you're like me, you probably love Docker. This role lets you install a
specific version of Docker as well as Docker Compose.

## Role variables

Below is a list of default values along with a description of what they do.

```
---

# This role only supports Docker 1.10.0 and above, also make sure you include
# the trailing .0 for versions that end in 0, such as 1.12.0.
docker_version: '1.12.1'

# Optionally install a specific version of Docker Compose.
docker_install_docker_compose: True
docker_compose_version: '1.8.1'

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
docker_apt_key: '58118E89F3A912897C070ADBF76221572C52609D'

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
docker_repository: 'deb https://apt.dockerproject.org/repo {{ docker_distribution | lower }}-{{ docker_distribution_release }} main'
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
