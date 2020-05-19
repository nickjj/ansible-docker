# Changelog

## v2.0.0

*Released: May 19th 2020*

- **Backwards incompatible change:** `python-docker` was renamed to `python3-docker`
- Fix symlink related issues with virtualenv when using virtualenv 20+
- Configure daemon before installing Docker to allow customizing certain things
- Support multiple CPU architecture types (amd64, arm64, armhf, armv7l)
- Officially support Ubuntu 20.04
- Remove all support for Python 2.x
- Officially remove support for Ubuntu 16.04

## v1.9.2

*Released: February 13th 2020*

- Add `gcc` as dependency since Docker Compose 1.25+ needs it
- Add `python(3)-dev` as dependency since Docker Compose 1.25+ needs it
- Fix Docker module import error so that you can use the `docker_*` Ansible modules

## v1.9.1

*Released: September 9th 2019*

- Fix quote mismatch when writing environment variable based systemd configuration

## v1.9.0

*Released: August 7th 2019*

- Officially support Debian Buster
- Fix version pinning to work for both the `docker-ce` and `docker-ce-cli` package
- Add `docker__cron_jobs_prune_schedule` to configure the docker system prune schedule
- Fix most Ansible 2.8.x warnings (purposely ignoring the apititude warning)

## v1.8.0

*Released: December 19th 2018*

- Change `docker__apt_key_server` to `docker__apt_key_url`
- `docker__version` and `docker__compose_version` are back to being empty strings by default

## v1.7.0

*Released: December 18th 2018*

- `docker__version` and `docker__compose_version` are now both undefined by default
- Change `docker__users` to default to `docker__users: ["{{ ansible_env.SUDO_USER | d('root') }}"]`
- Check for an existing Docker Compose file before trying to symlink it

## v1.6.0

*Released: December 15th 2018*

### Features

- Docker and Docker Compose can now be installed to their latest versions by default
- A Virtualenv will be created for any PIP packages that get installed
- The `docker-compose` package is installed through PIP (complete with latest / version pinning)
- The `docker` package is installed through PIP (all of Ansible's `docker_*` modules now work)
- Symlinks are created to put `docker-compose` and `python-docker` on the system's path
- Better documentation to demonstrate how to downgrade / upgrade Docker versions
- Docker login's config path can now be configured
- Overall improved documentation and tests

### Variables

- Remove `python-pip` from `docker__package_dependencies`
- Remove `docker__install_docker_compose`
- Remove `docker__compose_download_url`
- Remove `docker__default_daemon_json_log_max_size`
- Remove `docker__default_daemon_json_log_max_file`
- Add `docker__state` to control the Docker APT package's state
- Add `docker__pip_dependencies` to install various APT dependencies to run PIP
- Add `docker__pip_virtualenv` to create a Virtualenv for PIP
- Add `docker__default_pip_packages` to install default PIP packages
- Add `docker__pip_packages` to install additional PIP packages
- Add `docker__pip_docker_compose_state` to control the Docker Compose PIP package's state
- Add `docker__pip_docker_state` to control the Docker PIP package's state
- Add `config_path` property to the `docker__registries` list
- Add `docker__cron_jobs_prune_flags` to configure which prune flags get set
- Change `docker__default_daemon_json` to log to journald by default
- Change `docker__channel` from being a string to a list

## v1.5.0

*Released: November 11th 2018*

- Rename `docker__install_docker__compose` to `docker__install_docker_compose`
- Bump Docker Compose version to 1.23
- Change systemd options to use `-H unix://` to be compatible with 18.09 by default
- Install `python-pip` apt package as a dependency for pip installing `docker`
- Pip install `docker` so Ansible's `docker_login` and `docker_service` modules work
- Remove unnecessary "Remove Upstart config file" task
- Remove unnecessary "Install Python for managing Docker login credentials" task
- Remove unnecessary `enabled: true` in the systemd restart handler (it starts on boot by default)

## v1.4.0

*Released: October 31st 2018*

- Rename `docker__daemon_options` to `docker__daemon_json`
- Rename `docker__daemon_options_log_max_size` to `docker__default_daemon_json_log_max_size`
- Rename `docker__daemon_options_log_max_file` to `docker__default_daemon_json_log_max_file`
- Add `docker__daemon_flags` for setting systemd unit file Docker daemon options
- Add `docker__systemd_override` for setting custom systemd directives for the Docker service
- Rename `docker__cron_tasks` to `docker__cron_jobs`
- `cron_file` can now be configured with cron jobs to write out cron jobs in `/etc/cron.d`
- Add `user` to cron jobs since we're now using `cron_file`
- Drastically improve documentation

## v1.3.0

*Released: October 21st 2018*

- Variables are now using the `docker__*` style instead of `docker_*`
- Add configuration value for Docker Compose download URL
- Make style changes based on yamllint and ansible-lint

## v1.2.0

*Released: October 11th 2018*

- Remove ability to remove the `docker-*` package
- Add documentation on how to remove Docker if you need to downgrade versions
- Let Docker manage its own systemd unit file
- Allow environment configuration using the systemd `docker.service.d/*` pattern

## v1.1.0

*Released: October 9th 2018*

- Add `-H fd://` to the daemon options at the systemd unit file level
- Update systemd unit file as per Docker's latest settings
- Convert to using `/etc/docker/daemon.json` for setting daemon options
- Add variables to configure log size and max number of files
- Default to rotating logs after 10 gigs of space is used (was previously unlimited)
- System prune cron job now sets the `-a` flag to remove unused images

## v1.0.0

*Released: September 19th 2018*

- Update role to be compliant and depend on Ansible 2.5+
- Add official support for Ubuntu 16.04 / 18.04 and Debian Jessie / Stretch
- Default to Docker v18.06
- Default to Docker Compose v1.22
- Default to the stable channel instead of edge
- Add support for configuring 1 or more registries (thanks to @Mykhailo Chalyi for starting this)
- Add ability to remove Docker by setting `docker__remove_package: True`
- Fix APT GPG key issues (thanks to @bidossessi for starting this)
- Add proper version pinning support
- Remove `docker__apt_package_name` because the package name has been simplified thanks to pinning
- Redirect system prune's cron output to `/dev/null`
- Extract Docker's package dependencies into `docker__package_dependencies`
- Add more tests

## v0.2.3

*Released: April 13th 2018*

- Default to Docker v18.04
- Default to Docker Compose v1.21
- Expose `docker__apt_package_name` to customize the APT package name

## v0.2.2

*Released: March 28th 2018*

- Default to Docker v18.03
- Default to Docker Compose v1.20

## v0.2.1

*Released: February 14th 2018*

- Default to Docker v18.02
- Default to Docker Compose v1.19

## v0.2.0

*Released: January 25th 2018*

- Change version strategy to be separate from Docker releases (it was a bad idea!)
- Change `docker__options` to `docker__daemon_options`
- Default to Docker v18.01 on the CE edge channel
- Fix systemd service so Docker loads after `network-online.target` instead of `network.target`
- Add cron job to clean up after Docker
- Add proper tests and support for Ubuntu 16, Debian Stretch and Debian Jessie
- Update format and style consistencies

## v17.12

*Released: January 11th 2018*

- Default to Docker v17.12 on the CE edge channel
- Default to Docker Compose v1.18

## v17.06

*Released: June 28th 2017*

- Default to Docker v17.06 on the CE edge channel
- Default to Docker Compose v1.14
- Update code base to support Docker's new version format

## v0.1.2

*Released: October 9th 2016*

- Fix apt.cache https could not be found error

## v0.1.1

*Released: October 9th 2016*

- Fix issue where `docker-engine` package was not found

## v0.1.0

*Released: October 8th 2016*

- Initial release
