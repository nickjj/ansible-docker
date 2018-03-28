# Changelog

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
