# Changelog

### v1.0.0

*Released: September 19th 2018*

- Update role to be compliant and depend on Ansible 2.5+
- Add official support for Ubuntu 16.04 / 18.04 and Debian Jessie / Stretch
- Default to Docker v18.06
- Default to Docker Compose v1.22
- Default to the stable channel instead of edge
- Add support for configuring 1 or more registries (thanks to @Mykhailo Chalyi for starting this)
- Add ability to remove Docker by setting `docker_remove_package: True`
- Fix APT GPG key issues (thanks to @bidossessi for starting this)
- Add proper version pinning support
- Remove `docker_apt_package_name` because the package name has been simplified thanks to pinning
- Redirect system prune's cron output to `/dev/null`
- Extract Docker's package dependencies into `docker_package_dependencies`
- Add more tests

### v0.2.3

*Released: April 13th 2018*

- Default to Docker v18.04
- Default to Docker Compose v1.21
- Expose `docker_apt_package_name` to customize the APT package name

### v0.2.2

*Released: March 28th 2018*

- Default to Docker v18.03
- Default to Docker Compose v1.20

### v0.2.1

*Released: February 14th 2018*

- Default to Docker v18.02
- Default to Docker Compose v1.19

### v0.2.0

*Released: January 25th 2018*

- Change version strategy to be separate from Docker releases (it was a bad idea!)
- Change `docker_options` to `docker_daemon_options`
- Default to Docker v18.01 on the CE edge channel
- Fix systemd service so Docker loads after `network-online.target` instead of `network.target`
- Add cron job to clean up after Docker
- Add proper tests and support for Ubuntu 16, Debian Stretch and Debian Jessie
- Update format and style consistencies

### v17.12

*Released: January 11th 2018*

- Default to Docker v17.12 on the CE edge channel
- Default to Docker Compose v1.18

### v17.06

*Released: June 28th 2017*

- Default to Docker v17.06 on the CE edge channel
- Default to Docker Compose v1.14
- Update code base to support Docker's new version format

### v0.1.2

*Released: October 9th 2016*

- Fix apt.cache https could not be found error

### v0.1.1

*Released: October 9th 2016*

- Fix issue where `docker-engine` package was not found

### v0.1.0

*Released: October 8th 2016*

- Initial release
