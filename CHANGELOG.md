# Changelog

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
