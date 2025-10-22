## 🐳 What is ansible-docker?

It is an [Ansible](http://www.ansible.com/home) role to:

- Install Docker (channels and version pinning are supported)
- Install Docker Compose v2 (version pinning is supported)
- Install the `docker` PIP package so Ansible's `docker_*` modules work
- Manage Docker registry login credentials
- Configure 1 or more users to run Docker without needing root access
- Configure the Docker daemon's options and environment variables
- Configure a cron job to run Docker clean up commands

## ❔ Why would you want to use this role?

If you're like me, you probably love Docker. This role provides everything you
need to get going with a production ready Docker host.

By the way, if you don't know what Docker is, or are looking to become an expert
with it then check out
[Dive into Docker: The Complete Docker Course for Developers](https://diveintodocker.com/?utm_source=ansibledocker&utm_medium=github&utm_campaign=readmetop).

## 🛟 Supported platforms

- Ubuntu 22.04 LTS (Jammy Jellyfish)
- Ubuntu 24.04 LTS (Noble Numbat)
- Debian 11 (Bullseye)
- Debian 12 (Bookworm)

Previous releases may or may not work but they're not officially supported.

---

*You are viewing the master branch's documentation which might be ahead of the
latest release. [Switch to the latest release](https://github.com/nickjj/ansible-docker/tree/v2.5.2).*

---

## ✨ Quick start

The philosophy for all of my roles is to make it easy to get going, but provide
a way to customize nearly everything.

### What's configured by default?

The latest stable release of Docker CE and Docker Compose v2 will be installed,
Docker disk clean up will happen once a week and Docker container logs will be
sent to `journald`.

### Example playbook

```yml
---

# docker.yml

- name: Example
  hosts: "all"
  become: true

  roles:
    - role: "nickjj.docker"
      tags: ["docker"]
```

Usage: `ansible-playbook docker.yml`

### Installation

`$ ansible-galaxy install nickjj.docker`

## ⚙️ Default role variables

### Installing Docker

#### Channel

Do you want to use the "stable" or "test" channel? You can add more than one
(order matters).

```yml
docker__channel: ["stable"]
```

#### Version

- When set to "", the current latest version of Docker will be installed
- When set to a specific version, that version of Docker will be installed and pinned

```yml
docker__version: ""

# For example, pin it to 28.0.
docker__version: "28.0"

# For example, pin it to a more precise version of 28.0.
docker__version: "28.2.1"
```

*Pins are set with `*` at the end of the package version so you will end up
getting minor and security patches unless you pin an exact version.*

##### Upgrade strategy

- When set to `"present"`, running this role in the future won't install newer
versions (if available)
- When set to `"latest"`, running this role in the future will install newer
versions (if available)

```yml
docker__state: "present"
```

##### Downgrade strategy

The easiest way to downgrade would be to uninstall the Docker package manually
and then run this role afterwards while pinning whatever specific Docker version
you want.

```sh
# An ad-hoc Ansible command to stop and remove the Docker CE package on all hosts.
ansible all -m systemd -a "name=docker-ce state=stopped" \
  -m apt -a "name=docker-ce autoremove=true purge=true state=absent" -b
```

### Installing Docker Compose v2

Docker Compose v2 will get apt installed using the official
`docker-compose-plugin` that Docker manages.

#### Version

- When set to "", the current latest version of Docker Compose v2 will be installed
- When set to a specific version, that version of Docker Compose v2 will be installed
and pinned

```yml
docker__compose_v2_version: ""

# For example, pin it to 2.36.
docker__compose_v2_version: "2.36"

# For example, pin it to a more precise version of 2.36.
docker__compose_v2_version: "2.36.2"
```

##### Upgrade strategy

It'll re-use the `docker__state` variable explained above in the Docker section
with the same rules.

##### Downgrade strategy

Like Docker itself, the easiest way to uninstall Docker Compose v2 is to manually
run the command below and then pin a specific Docker Compose v2 version.

```sh
# An ad-hoc Ansible command to remove the Docker Compose Plugin package on all hosts.
ansible all -m apt -a "name=docker-compose-plugin autoremove=true purge=true state=absent" -b
```

### Installing Docker Compose v1

By default this role doesn't install Docker Compose v1 since it's been
officially deprecated and no longer receives updates by Docker. However, this
role is capable of installing it. All you have to do is set
`docker__pip_docker_compose_state: "present"` since this role defaults to
`absent` for this value.

Technically both versions can be installed together since v1 is accessed with
`docker-compose` and v2 is accessed with `docker compose` (notice the lack of
hyphen).

I'd suggest not installing v1 unless you really need it for legacy purposes. If
you do decide to install it you can configure which version gets installed
below. If it's not set to be installed these versions are left unused:

#### Version

- When set to "", the current latest version of Docker Compose v1 will be installed
- When set to a specific version, that version of Docker Compose v1 will be installed
and pinned

```yml
docker__compose_version: ""

# For example, pin it to 1.29.
docker__compose_version: "1.29"

# For example, pin it to a more precise version of 1.29.
docker__compose_version: "1.29.2"
```

*Upgrade and downgrade strategies will be explained in the other section of this
README.*

### Configuring users to run Docker without root

A list of users to be added to the `docker` group.

Keep in mind this user needs to already exist, this role will not create it. If
you want to create users, check out my
[user role](https://github.com/nickjj/ansible-user).

This role does not configure User Namespaces or any other security features
by default. If the user you add here has SSH access to your server then you're
effectively giving them root access to the server since they can run Docker
without `sudo` and volume mount in any path on your file system.

In a controlled environment this is safe, but like anything security related
it's worth knowing this up front. You can enable User Namespaces and any
other options with the `docker__daemon_json` variable which is explained later.

```yml
# Try to use the sudo user by default, but fall back to root.
docker__users: ["{{ ansible_env.SUDO_USER | d('root') }}"]

# For example, if the user you want to set is different than the sudo user.
docker__users: ["admin"]
```

### Configuring Docker registry logins

Login to 1 or more Docker registries (such as the
[Docker Hub](https://hub.docker.com/)).

```yml
# Your login credentials will end up in this user's home directory.
docker__login_become_user: "{{ docker__users | first | d('root') }}"
```

```yml
# 0 or more registries to log into.
docker__registries:
  - #registry_url: "https://index.docker.io/v1/"
    username: "your_docker_hub_username"
    password: "your_docker_hub_password"
    #email: "your_docker_hub@emailaddress.com"
    #reauthorize: false
    #config_path: "$HOME/.docker/config.json"
    #state: "present"
docker__registries: []
```

*Properties prefixed with \* are required.*

- `registry_url` defaults to `https://index.docker.io/v1/`
- *`username` is your Docker registry username
- *`password` is your Docker registry password
- `email` defaults to not being used (not all registries use it)
- `reauthorize` defaults to `false`, when `true` it updates your credentials
- `config_path` defaults to your `docker__login_become_user`'s `$HOME` directory
- `state` defaults to "present", when "absent" the login will be removed

### Configuring the Docker daemon options (json)

Default Docker daemon options as they would appear in `/etc/docker/daemon.json`.

```yml
docker__default_daemon_json: |
  "log-driver": "journald",
  "features": {
    "buildkit": true
  }

# Add your own additional daemon options without overriding the default options.
# It follows the same format as the default options, and don't worry about
# starting it off with a comma. The template will add the comma if needed.
docker__daemon_json: ""
```

#### Alternative dict-based approach

```yml
docker__daemon_json_dict:
  log-driver: journald
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

If you know what you're doing, you can override or add to any of Docker's systemd
directives by setting this variable. Anything you place in this string will be
written to `/etc/systemd/system/docker.service.d/custom.conf` as is.

```yml
docker__systemd_override: ""
```

### Configuring Docker related cron jobs

By default this will safely clean up disk space used by Docker every Sunday at
midnight.

```yml
# `a` removes unused images (useful in production).
# `f` forces it to happen without prompting you to agree.
docker__cron_jobs_prune_flags: "af"

# Control the schedule of the docker system prune.
docker__cron_jobs_prune_schedule: ["0", "0", "*", "*", "0"]

docker__cron_jobs:
  - name: "Docker disk clean up"
    job: "docker system prune -{{ docker__cron_jobs_prune_flags }} > /dev/null 2>&1"
    schedule: "{{ docker__cron_jobs_prune_schedule }}"
    cron_file: "docker-disk-clean-up"
    #user: "{{ (docker__users | first) | d('root') }}"
    #state: "present"
```

*Properties prefixed with \* are required.*

- *`name` is the cron job's description
- *`job` is the command to run in the cron job
- *`schedule` is the [standard cron job](https://en.wikipedia.org/wiki/Cron#Overview)
format for every Sunday at midnight
- *`cron_file` writes a cron file to `/etc/cron.d` instead of a user's individual crontab
- `user` defaults to the first `docker__users` user or root if that's not available
- `state` defaults to "present", when "absent" the cron file will be removed

### Configuring the APT package manager

Docker requires a few dependencies to be installed for it to work. You shouldn't
have to edit any of these variables.

```yml
# List of packages to be installed.
docker__package_dependencies:
  - "apt-transport-https"
  - "ca-certificates"
  - "cron"
  - "gnupg2"
  - "software-properties-common"

# Ansible identifies CPU architectures differently than Docker.
docker__architecture_map:
  "x86_64": "amd64"
  "aarch64": "arm64"
  "aarch": "arm64"
  "armhf": "armhf"
  "armv7l": "armhf"

# The Docker GPG key URL.
docker__apt_repository_url: "https://download.docker.com/linux/{{ ansible_distribution | lower }}"

# The Docker GPG key checksum value.
docker__apt_key_checksum: "sha256:1500c1f56fa9e26b9b8f42452a553675796ade0807cdce11975eb98170b3a570"

# The Docker upstream APT repository.
docker__apt_repository: >
  deb [arch={{ docker__architecture_map[ansible_architecture] }}
  signed-by=/etc/apt/keyrings/docker.asc]
  {{ docker__apt_repository_url }}
  {{ ansible_distribution_release }} {{ docker__channel | join(' ') }}
```

### Installing Python packages with Virtualenv and PIP

#### Configuring Virtualenv

Rather than pollute your server's version of Python, all PIP packages are
installed into a Virtualenv of your choosing.

```yml
docker__pip_virtualenv: "/usr/local/lib/docker/virtualenv"
```

#### Installing PIP and its dependencies

This role installs PIP because Docker Compose v1 is installed with the
`docker-compose` PIP package and Ansible's `docker_*` modules use the `docker`
PIP package.

```yml
docker__pip_dependencies:
  - "gcc"
  - "python3-setuptools"
  - "python3-dev"
  - "python3-pip"
  - "virtualenv"
```

#### Installing PIP packages

```yml
docker__default_pip_packages:
  - name: "docker"
    state: "{{ docker__pip_docker_state }}"
  - name: "docker-compose"
    version: "{{ docker__compose_version }}"
    path: "/usr/local/bin/docker-compose"
    src: "{{ docker__pip_virtualenv + '/bin/docker-compose' }}"
    state: "{{ docker__pip_docker_compose_state }}"

# Add your own PIP packages with the same properties as above.
docker__pip_packages: []
```

*Properties prefixed with \* are required.*

- *`name` is the package name
- `version` is the package version to be installed (or "" if this is not defined)
- `path` is the destination path of the symlink
- `src` is the source path to be symlinked
- `state` defaults to "present", other values can be "forcereinstall" or "absent"

##### PIP package state

- When set to `"present"`, the package will be installed but not updated on
future runs
- When set to `"forcereinstall"`, the package will always be (re)installed and
updated on future runs
- When set to `"absent"`, the package will be skipped or removed

```yml
docker__pip_docker_state: "present"
docker__pip_docker_compose_state: "absent"
```

#### Working with Ansible's `docker_*` modules

This role uses `docker_login` to login to a Docker registry, but you may also
use the other `docker_*` modules in your own roles. They are not going to work
unless you instruct Ansible to use this role's Virtualenv.

At either the inventory, playbook or task level you'll need to set
`ansible_python_interpreter: "/usr/local/bin/python3-docker"`. This works
because this role creates a proxy script from the Virtualenv's Python binary to
`python3-docker`.

You can look at this role's `docker_login` task as an example on how to do it
at the task level.

## 👀 About the author

- Nick Janetakis | <https://nickjanetakis.com> | [@nickjanetakis](https://twitter.com/nickjanetakis)

I'm a self taught developer and have been freelancing for the last ~20 years.
You can read about everything I've learned along the way on my site at
[https://nickjanetakis.com](https://nickjanetakis.com/).

There's hundreds of [blog posts](https://nickjanetakis.com/blog) and a couple
of [video courses](https://nickjanetakis.com/courses) on web development and
deployment topics. I also have a [podcast](https://runninginproduction.com)
where I talk with folks about running web apps in production.
