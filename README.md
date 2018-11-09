## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to:

- Install Docker (editions, channels and version pinning are all supported)
- Install Docker Compose
- Manage login credentials for 1 or more public or private Docker registries
- Configure 1 or more users to run Docker without needing root access
- Configure the Docker daemon's options and environment variables
- Configure a cron job to run Docker clean up commands

## Why would you want to use this role?

If you're like me, you probably love Docker. This role provides everything you
need to get going with a production ready Docker host.

By the way, if you don't know what Docker is, or are looking to become an expert
with it then check out
[Dive into Docker: The Complete Docker Course for Developers](https://diveintodocker.com/?utm_source=ansibledocker&utm_medium=github&utm_campaign=readmetop).

## Supported platforms

- Ubuntu 16.04 LTS (Xenial)
- Ubuntu 18.04 LTS (Bionic)
- Debian 8 (Jessie)
- Debian 9 (Stretch)

---

*You are viewing the master branch's documentation which might be ahead of the
latest release. [Switch to the latest release](https://github.com/nickjj/ansible-docker/tree/v1.4.0).*

---

## Quick start

The philosophy for all of my roles is to make it easy to get going, but provide
a way to customize nearly everything.

### What's configured by default?

The latest Docker CE will be installed, Docker Compose will be installed, Docker
disk clean up will happen once a week and Docker container logs will be rotated
at `1mb` file sizes `10,000` times (10GB of disk space will be used at max).

### Example playbook

```yml
---

# site.yml

- name: Example
  hosts: "all"
  become: true

  roles:
    - { role: "nickjj.docker", tags: ["docker"] }
```

Usage: `ansible-playbook site.yml -t docker`

### Installation

`$ ansible-galaxy install nickjj.docker`

## Default role variables

### Installing Docker

```yml
# Do you want to use "ce" (community edition) or "ee" (enterprise edition)?
docker__edition: "ce"

# Do you want to use the "stable", "edge", "testing" or "nightly" channels?
# Add more than 1 channel by separating each one with a space.
docker__channel: "stable"

# When set to "latest" this role will always attempt to install the latest
# version based on the channel you selected. This could lead to something like
# Docker 18.06 being installed today but then a year from now, re-running the
# role will result in 19.06 or whatever Docker happens to use a year from now.
#
# If you want to pin a version simply put "18.06", "18.06.1" or whatever version
# you want. Even if you update your package list and newer Docker versions are
# available this role will stick to the pinned version on all future runs.
docker__version: "latest"
```

### Installing Docker Compose

```yml
# Do you want to also install Docker Compose? When set to False, Docker Compose
# will not get installed or will be removed if it were installed previously.
docker__install_docker_compose: true

# If Docker Compose is being installed, which version do you want to use?
docker__compose_version: "1.23.0"

# If Docker Compose is being installed, where should it be downloaded from?
docker__compose_download_url: "https://github.com/docker/compose/releases/download/{{ docker__compose_version }}/docker-compose-Linux-x86_64"
```

### Configuring users to run Docker without root

A list of users to be added to the `docker` group.

Keep in mind this user needs to already exist, this role will not create it. If
you want to create users, check out my
[user role](https://github.com/nickjj/ansible-user).

This role does not configure User Namespaces or any other security features
by default. If the user you add here has SSH access to your server then you're
effectively giving them root access to the server since they can run Docker
without sudo and volume mount in any path on your file system.

In a controlled environment this is safe, but like anything security related
it's worth knowing this up front. You can enable User Namespaces and any
other options with the `docker__daemon_json` variable which is explained later.

```yml
docker__users: []

# For example, if you have a user of "admin" you could set this.
docker__users: ["admin"]
```

### Configuring Docker registry logins

Login to 1 or more Docker registries (such as the
[Docker Hub](https://hub.docker.com/)) so that the Docker CLI can interact
with private repos.

```yml
docker__registries:
  - #registry_url: "https://index.docker.io/v1/"
    username: "your_docker_hub_username"
    password: "your_docker_hub_password"
    #email: "your_docker_hub@emailaddress.com"
    #reauthorize: false
    #system_user: "root"
    #state: "present"
docker__registries: []
```

*Items prefixed with \* are required.*

- `registry_url` defaults to `https://index.docker.io/v1/`
- *`username` is your Docker registry username
- *`password` is your Docker registry password
- `email` defaults to not being used (not all registries use it)
- `reauthorize` defaults to `false`, when `true` it updates your credentials
- `system_user` defaults to the first user in `docker__users` OR `"root"` if that's
empty
- `state` defaults to "present", when "absent" the login will be removed

### Configuring log rotation for Docker container logs

```yml
# How large should each Docker log file be? You can set -1 for unlimited.
#
# You can use "k" to denote kilobytes, "m" for megabytes and "g" for gigabytes.
#
# Here's 3 example sizes showcasing the format: 100k, 100m and 10g
docker__default_daemon_json_log_max_size: "1m"

# Docker rotates its own container logs. How many rotations do you want to keep
# on disk? With a size of 1m and 10,000 rotations, that would be a max of 10gb
# of disk space.
docker__default_daemon_json_log_max_file: 10000
```

### Configuring the Docker daemon options (json)

Default Docker daemon options as they would appear in `/etc/docker/daemon.json`.

```yml
docker__default_daemon_json: |
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "{{ docker__default_daemon_json_log_max_size }}",
    "max-file": "{{ docker__default_daemon_json_log_max_file }}"
  }

# Add your own additional daemon options without overriding the default options.
# It follows the same format as the default options, and don't worry about
# starting it off with a comma. The template will add the comma if needed.
docker__daemon_json: ""
```

### Configure the Docker daemon options (flags)

Flags that are set when starting the Docker daemon cannot be changed in the
`daemon.json` file. By default Docker sets `-H unix://` which means that option
cannot be changed with the json options.

Add or change the starting Docker daemon flags by supplying them exactly how
they would appear on the command line.

```yml
# Each command line flag should be its own item in the list.
#
# Using a Docker version prior to 18.09?
#   You must set `-H fd://` instead of `-H unix://`.
docker__daemon_flags:
  - "-H unix://"
```

*If you don't supply some type of `-H` flag here, Docker will fail to start.*

### Configuring the Docker daemon environment variables

```yml
docker__daemon_environment: []

# For example, here's how to set a couple of proxy environment variables.
docker__daemon_environment:
  - "HTTP_PROXY=http://proxy.example.com:80"
  - "HTTPS_PROXY=https://proxy.example.com:443"
```

### Configuring advanced systemd directives

This role lets the Docker package manage its own systemd unit file and adjusts
things like the Docker daemon flags and environment variables by using
the systemd override pattern.

If you know what you're doing, you can override any of Docker's systemd
directives by setting this variable. Anything you place in this string will be
written to `/etc/systemd/system/docker.service.d/custom.conf` as is.

```yml
docker__systemd_override: ""
```

### Configuring Docker related cron jobs

By default this will safely clean up disk space used by Docker every Sunday at
midnight. Keep in mind the `-a` flag will remove unused images which is useful
if you version your images (that can really add up in disk space).

```yml
docker__cron_jobs:
  - name: "Docker disk clean up"
    job: docker system prune -af &> /dev/null
    schedule: ["0", "0", "*", "*", "0"]
    cron_file: "docker-disk-clean-up"
    #user: "{{ (docker__users | first) | default('root') }}"
    #state: "present"
```

*Items prefixed with \* are required.*

- *`name` is the cron job's description
- *`job` is the command to run in the cron job
- *`schedule` is the [standard cron job](https://en.wikipedia.org/wiki/Cron#Overview)
format for every Sunday at midnight
- *`cron_file` writes a cron file to `/etc/cron.d` instead of a user's individual crontab
- `user` defaults to the first user in `docker__users` OR `root` if the users list is empty
- `state` defaults to "present", when "absent" the cron file will be removed

### Configuring the APT package manager

Docker requires a few dependencies to be installed for it to work. You shouldn't
have to edit any of these settings.

If you're curious about `python-pip`, it's because Ansible's `docker_login` and
`docker_service` modules require installing the `docker` pip package.

```yml
docker__package_dependencies:
  - "apt-transport-https"
  - "ca-certificates"
  - "cron"
  - "gnupg2"
  - "python-pip"
  - "software-properties-common"

# The Docker GPG key id used to sign the Docker package.
docker__apt_key_id: "9DC858229FC7DD38854AE2D88D81803C0EBFCD88"

# The Docker GPG key server address.
docker__apt_key_server: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"

# The Docker APT repository.
docker__apt_repository: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker__channel }}"
```

## Trying to figure out how to downgrade Docker?

If you want to downgrade Docker, the easiest way to do it would be to uninstall
the Docker package manually and then run this role afterwards while pinning
whatever specific Docker version you want.

```sh
# An ad-hoc Ansible command to remove the Docker CE package on all hosts.
ansible all -m apt -a "name=docker-ce state=absent purge=true"
```

## License

MIT
