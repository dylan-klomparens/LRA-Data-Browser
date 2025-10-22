# LRA Data Browser

# Required system packages
* Caddy (for reverse proxy and TLS support)
* Python

## Important files and directories

* `/opt/LRA-Data-Browser` - Streamlit app directory
* `/etc/caddy/Caddyfile` - Reverse proxy configuration file
* `/etc/systemd/system/lra-data-browser.service` - Systemd service configuration file

## Maintenance commands

Streamlit app:
* Start: `systemctl start lra-data-browser.service`
* Stop: `systemctl stop lra-data-browser.service`
* Status: `systemctl status lra-data-browser.service`
* Update from git repository: `cd /opt/LRA-Data-Browser` and `git pull`

Caddy reverse proxy:
* Start: `systemctl start lra-data-browser.service`
* Stop: `systemctl stop lra-data-browser.service`
* Status: `systemctl status lra-data-browser.service`

## Virtual machine configuration

Caddy reverse proxy is installed as a system package. The configuration resides in `/etc/caddy/Caddyfile`.

The Streamlit app resides in `/opt/LRA-Data-Browser`. That folder also contains its own Python virtual environment, in `/opt/LRA-Data-Browser/.venv`. The Streamlit app is run using a systemd service, whose configuration resides at `/etc/systemd/system/lra-data-browser.service`.

