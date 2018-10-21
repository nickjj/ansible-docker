## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to:

- Install Docker (editions, channels and version pinning are all supported)
- Install Docker Compose
- Manage login credentials for 1 or more public or private Docker registries
- Configure 1 or more users to run Docker without needing root access
- Configure a cron job to run Docker clean up commands
- Configure the Docker daemon's options and environment variables

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

## Role variables

```
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

# Do you want to also install Docker Compose? When set to False, Docker Compose
# will not get installed or will be removed if it were installed previously.
docker__install_docker__compose: True

# If Docker Compose is being installed, which version do you want to use?
docker__compose_version: "1.22.0"

# If Docker Compose is being installed, where should it be downloaded from?
docker__compose_download_url: "https://github.com/docker/compose/releases/download/{{ docker__compose_version }}/docker-compose-Linux-x86_64"

# A list of users to be added to the docker group. For example if you have a
# user of "admin", then you'll want to set docker__users: ["admin"] here.
#
# Keep in mind this user needs to already exist, this role will not create it.
#
# This role does not configure User Namespaces or any other security features
# by default. If the user you add here has SSH access to your server then you're
# effectively giving them root access to the system since they can run docker
# without sudo and volume mount in any file on your file system.
#
# In a controlled environment this is safe, but like anything security related
# it's worth knowing this up front. You can enable User Namespaces and any
# other options with the docker__daemon_options variable which is explained later.
docker__users: []

# Manage login credentials for 1 or more Docker registries. Example usage:
# docker__registries:
#     # Your registry URL is optional and defaults to the Docker Hub if undefined.
#   - registry_url: "https://index.docker.io/v1/"
#     # Your username is required.
#     username: "your_docker__hub_username"
#     # Your password is required.
#     password: "your_docker__hub_password"
#     # Your email address is optional (not all registries use it).
#     email: "your_docker__hub@emailaddress.com"
#     # Update your credentials. If undefined, this behavior will be skipped.
#     reauthorize: False
#     # Remove a login by setting an absent state (it defaults to present).
#     state: "absent"
#     # The system user that will have access to the registry. If undefined it
#     # will default to the root user. You likely want to set this to be a user
#     # defined in your docker__users list above.
#     system_user: "a_user_defined_in_docker__users"
docker__registries: []

# How large should each Docker log file be? You can set -1 for unlimited.
#
# You can use "k" to denote kilobytes, "m" for megabytes and "g" for gigabytes.
# Here's 3 example sizes showcasing the format: 100k, 100m and 10g
docker__daemon_options_log_max_size: "10m"

# Docker rotates its own logs. How many rotations do you want to keep on disk?
# With a size of 10m and 1000 rotations, that would be a max of 10gb of disk space.
docker__daemon_options_log_max_file: 1000

# Default Docker daemon options as they would appear in /etc/docker/daemon.json.
# In this example, we're setting the log rotate related flags.
docker__daemon_default_options: |
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "{{ docker__daemon_options_log_max_size }}",
    "max-file": "{{ docker__daemon_options_log_max_file }}"
  }

# Add your own additional daemon options without overriding the default options.
# It follows the same format as the default options, and don't worry about
# starting it off with a comma. The template will add the comma if needed.
docker__daemon_options: ""

# Can be used to set environment variables for the Docker daemon, such as:
# docker__daemon_environment:
#   - "HTTP_PROXY=http://proxy.example.com:80"
#   - "HTTPS_PROXY=https://proxy.example.com:443"
docker__daemon_environment: []

# Manage 1 or more cron jobs to perform Docker related system tasks. By default
# this will safely clean up disk space used by Docker every Sunday at midnight.
docker__cron_tasks:
  - job: docker system prune -af &> /dev/null
    name: "Docker disk clean up"
    schedule: ["0", "0", "*", "*", "0"]
    # Remove a cron task by setting an absent state (it defaults to present).
    # state: "absent"

# A list of packages that Docker requires to run. Typically you shouldn't have
# to modify this list, but if Docker's dependencies change it can be updated
# here without having to fork the role.
docker__package_dependencies:
  - "apt-transport-https"
  - "ca-certificates"
  - "software-properties-common"
  - "gnupg2"
  - "cron"

# The Docker GPG key id used to sign the Docker package.
docker__apt_key_id: "9DC858229FC7DD38854AE2D88D81803C0EBFCD88"

# The Docker GPG key server address.
docker__apt_key_server: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"

# The Docker APT repository.
docker__apt_repository: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker__channel }}"
```

## Example usage

For the sake of this example let's assume you have a group called **app** and
you have a typical `site.yml` file.

To use this role edit your `site.yml` file to look something like this:

```
---

- name: Configure app server(s)
  hosts: "app"
  become: True

  roles:
    - { role: "nickjj.docker", tags: ["docker"] }
```

Here's a few examples. You can recreate this example on your end by opening or
creating `group_vars/app.yml` which is located relative to your `inventory`
directory and  then making it look like this:

```
---

# Pin Docker version 18.06 from the stable channel.
docker__version: "18.06"

# Allow the admin and zerocool users to access Docker without needing root access.
docker__users: ["admin", "zerocool"]

# A couple of examples of authenticating to a Docker registry.
docker__registries:
  # Authenticate to the Docker Hub, and allow the "admin" system user acces to it:
  - username: "your_docker_hub_username"
    password: "your_docker_hub_password"
    email: "your_docker_hub@emailaddress.com"
    system_user: "{{ docker__users | first }}"
  # Authenticate to some other private registry and allow "zerocool":
  - registry_url: "https://your-registry.com"
    username: "some_other_username"
    password: "some_other_password"
    system_user: "zerocool"
  # Disable logging in to some old registry you don't use anymore:
  - registry_url: "https://old-registry.com"
    username: "some_old_username"
    password: "some_old_password"
    state: "absent"
```

*If you're looking for an Ansible role to create users, then check out my
[user role](https://github.com/nickjj/ansible-user)*.

Now you would run `ansible-playbook -i inventory/hosts site.yml -t docker`.

#### Trying to figure out how to downgrade Docker?

If you want to downgrade Docker, the easiest way to do it would be to uninstall
the Docker package manually and then run this role afterwards while pinning
whatever specific Docker version you want.

Here's an adhoc Ansible command to remove the Docker CE package on the `app` hosts:  
`ansible app -i inventory/hosts -m apt -a "name=docker-ce state=absent purge=true"`

## Installation

`$ ansible-galaxy install nickjj.docker`

## Ansible Galaxy

You can find it on the official
[Ansible Galaxy](https://galaxy.ansible.com/nickjj/docker/) if you want to
rate it.

## License

MIT
