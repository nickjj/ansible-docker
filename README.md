## What is ansible-docker? [![Build Status](https://secure.travis-ci.org/nickjj/ansible-docker.png)](http://travis-ci.org/nickjj/ansible-docker)

It is an [Ansible](http://www.ansible.com/home) role to:

- Install Docker (editions, channels and version pinning are all supported)
- Install Docker Compose
- Manage login credentials for 1 or more public or private Docker registries
- Set up 1 or more users to run Docker without needing root access
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
# When set to "True", the Docker package and supporting files will be removed.
docker_remove_package: False

# Do you want to use "ce" (community edition) or "ee" (enterprise edition)?
docker_edition: "ce"

# Do you want to use the "stable", "edge", "testing" or "nightly" channels?
# Add more than 1 channel by separating each one by a space.
docker_channel: "stable"

# When set to "latest" this role will always attempt to install the latest
# version based on the channel you selected. This could lead to something like
# Docker 18.06 being installed today but then a year from now, re-running the
# role will result in 19.06 or whatever Docker happens to use a year from now.
#
# If you want to pin a version simply put "18.06", "18.06.1" or whatever version
# you want. Even if you update your package list and newer Docker versions are
# available this role will stick to the pinned version on all future runs.
docker_version: "latest"

# Do you want to also install Docker Compose?
docker_install_docker_compose: True

# If Docker Compose is being installed, which version do you want to use?
docker_compose_version: "1.22.0"

# A list of users to be added to the docker group. For example if you have a
# user of "admin", then you'll want to set docker_users: ["admin"] here.
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
# other options with the docker_daemon_options variable which is explained later.
docker_users: []

# Manage login credentials for 1 or more Docker registries. Example usage:
# docker_registries:
#     # Your registry URL is optional and defaults to the Docker Hub if undefined.
#   - registry_url: "https://index.docker.io/v1/"
#     # Your username is required.
#     username: "your_docker_hub_username"
#     # Your password is required.
#     password: "your_docker_hub_password"
#     # Your email address is optional (not all registries use it).
#     email: "your_docker_hub@emailaddress.com"
#     # Update your credentials. If undefined, this behavior will be skipped.
#     reauthorize: False
#     # Enable or disable these credentials by setting "present" or "absent".
#     # If undefined, it will default to "present".
#     state: "present"
#     # The system user that will have access to the registry. If undefined it
#     # will default to the root user. You likely want to set this to be a user
#     # defined in your docker_users list above.
#     system_user: "a_user_defined_in_docker_users"
docker_registries: []

# Docker daemon options as they would appear on the command line, such as:
# docker_daemon_options:
#   - "--dns 8.8.8.8"
docker_daemon_options: []

# Can be used to set environment variables for the Docker daemon, such as:
# docker_daemon_environment:
#   - "HTTP_PROXY=http://proxy.example.com:3128/"
#   - "HTTPS_PROXY=http://proxy.example.com:3128/"
#   - "NO_PROXY=localhost,127.0.0.1"
docker_daemon_environment: []

# Manage 1 or more cron jobs to perform Docker related system tasks. By default
# this will safely clean up disk space used by Docker every Sunday at midnight.
docker_cron_tasks:
  - job: docker system prune -f &> /dev/null
    name: "Docker disk clean up"
    schedule: ["0", "0", "*", "*", "0"]

# A list of packages that Docker requires to run. Typically you shouldn't have
# to modify this list, but if Docker's dependencies change it can be updated
# here without having to fork the role.
docker_package_dependencies:
  - "apt-transport-https"
  - "ca-certificates"
  - "software-properties-common"
  - "gnupg2"
  - "cron"

# The Docker GPG key id used to sign the Docker package.
docker_apt_key_id: "9DC858229FC7DD38854AE2D88D81803C0EBFCD88"

# The Docker GPG key server address.
docker_apt_key_server: "https://download.docker.com/linux/{{ ansible_distribution | lower }}/gpg"

# The Docker APT repository.
docker_apt_repository: "deb [arch=amd64] https://download.docker.com/linux/{{ ansible_distribution | lower }} {{ ansible_distribution_release }} {{ docker_channel }}"

# How long should the apt-cache last in seconds?
docker_apt_cache_time: 86400
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
docker_version: "18.06"

# Allow the admin and zerocool users to access Docker without needing root access.
docker_users: ["admin", "zerocool"]

# A couple of examples of authenticating to a Docker registry.
docker_registries:
  # Authenticate to the Docker Hub, and allow the "admin" system user acces to it:
  - username: "your_docker_hub_username"
    password: "your_docker_hub_password"
    email: "your_docker_hub@emailaddress.com"
    system_user: "{{ docker_users | first }}"
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

## Installation

`$ ansible-galaxy install nickjj.docker`

## Ansible Galaxy

You can find it on the official
[Ansible Galaxy](https://galaxy.ansible.com/nickjj/docker/) if you want to
rate it.

## License

MIT
