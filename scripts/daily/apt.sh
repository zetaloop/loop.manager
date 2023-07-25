# APT Daily Update & Autoremove & Purge

apt update
apt upgrade -y
apt autoremove
apt clean
dpkg -l | grep '^rc' | awk '{print $2}' | xargs -r dpkg --purge
