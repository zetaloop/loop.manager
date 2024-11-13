# SSH Config: KeepAlive

from utils.file import *

# Define the path to the sshd_config file
ssh = '/etc/ssh/sshd_config'

# The source is sshd_config and the destination is sshd_config appended with the current time.
with Backup(ssh, lambda: os.system('systemctl restart sshd')) as bak:

    # Read the lines of the sshd_config file into a list
    print(f'Reading {ssh}...')
    content = read(ssh)

    # Define the desired settings as a multiline string and split it into a list of lines
    items = [i + '\n' for i in '''
    TCPKeepAlive no
    ClientAliveInterval 3
    ClientAliveCountMax 20
    '''.split('\n') if i]

    # Loop over the lines in the settings list
    for item in items:
        # Split the line into its individual words
        it, *args = item.split()
        exist = False
        # Loop over the lines in the sshd_config file
        for i, ln in enumerate(content):
            # If the first word of the setting is in the sshd_config line and it is not commented out
            if it + ' ' in ln and '#' not in ln:
                # If it's the first occurrence, replace the line with the desired setting
                if not exist:
                    content[i] = item
                    exist = True
                # If it's not the first occurrence, comment out the line
                else:
                    content[i] = '# ' + ln
        # If the setting does not exist in the sshd_config file, append it
        if not exist:
            content.append(item)

    # Write the modified content back into the sshd_config file
    print(f'Writing {ssh}...')
    write(ssh, content)

    print(f'Show diff... {ssh} <<< {bak.backup_path}')
    diff(ssh, bak.backup_path)

print('\nRestarting sshd...')
if os.system('systemctl restart sshd'):
    print('\nRestarting failed! Restoring original config...')
    print(f'mv {ssh} >>> {ssh}_{time}_fail.bak')
    os.system(f'mv {ssh} {ssh}_{time}_fail.bak')
    print(f'mv {ssh} <<< {ssh}_{time}.bak')
    os.system(f'mv {ssh}_{time}.bak {ssh}')
    print('\nRestarting sshd...')
    if os.system('systemctl restart sshd'):
        print('\nError in original config!')
