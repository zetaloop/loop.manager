# Remove old linux kernels, you need to confirm the uninstallation

echo CURRENT KERNEL:
uname -r
echo Removing...
apt purge $(dpkg-query -W -f'${Package}\n' 'linux-*' | sed -nr 's/.*-([0-9]+(\.[0-9]+){2}-[^-]+).*/\1 &/p' | linux-version sort | awk '($1==c){exit} {print $2}' c=$(uname -r | cut -f1,2 -d-))
