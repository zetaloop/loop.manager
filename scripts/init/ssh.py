# SSH Config: KeepAlive, PersistWindow

import os
from datetime import datetime

# Get the current time and format it to a string in the format 'YYYYMMDD-HHMMSS'
time = datetime.now().strftime('%Y%m%d-%H%M%S')

# Define the path to the sshd_config file
ssh = '/etc/ssh/sshd_config'

# Inform the user about the backup creation process.
# The source is sshd_config and the destination is sshd_config appended with the current time.
print(f'Creating backup... {ssh} >>> {ssh}_{time}.bak')

# Use the os.system function to run a shell command that copies the sshd_config file to a backup file
os.system(f'cp {ssh} {ssh}_{time}.bak')

# Open the sshd_config file in read mode
print(f'Reading {ssh}...')
with open(ssh, 'r') as f:
    # Read the lines of the sshd_config file into a list
    content = f.readlines()

# Define the desired settings as a multiline string and split it into a list of lines
items = [i + '\n' for i in '''
TCPKeepAlive no
ServerAliveInterval 3
ServerAliveCountMax 20
ControlMaster auto
ControlPath ~/.ssh/connection-%r@%h:%p
ControlPersist 12h
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

# Open the sshd_config file in write mode
print(f'Writing {ssh}...')
with open(ssh, 'w') as f:
    # Write the modified content back into the sshd_config file
    f.writelines(content)

print(f'Show diff... {ssh} <<< {ssh}_{time}.bak')
os.system(f'diff {ssh} {ssh}_{time}.bak')
