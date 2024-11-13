import os
from datetime import datetime

__xpr = lambda x, : print('[FILE] ' + x)

def read(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    return content

def write(file_path, content):
    with open(file_path, 'w') as f:
        f.writelines(content)

def diff(file1, file2):
    os.system(f'diff {file1} {file2}')

class Backup:
    '''
    Create a backup context manager in utils_file.py that handles backup and restoration.
    It should automatically restore the backup if an exception occurs, unless .save() is called.
    '''
    def __init__(self, file_path, verify_command=None):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.backup_path = f"{file_path}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
        self.backup_name = os.path.basename(self.backup_path)
        self.verify_command = verify_command
        self.saved = False

    def __enter__(self):
        self.backup()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            __xpr(f"An error occurred ({exc_type}). Restoring backup...")
            self.restore()
        elif not self.saved:
            __xpr('Modification was interrupted. Restoring backup..."')
            self.restore()
        elif self.verify_command:
            self.verify_and_rollback()
        else:
            __xpr("Changes saved successfully.")

    def save(self):
        self.saved = True

    def backup(self):
        __xpr(f'Creating backup... {self.file_path} >>> {self.backup_path}')
        os.system(f'cp {self.file_path} {self.backup_path}')

    def restore(self):
        os.system(f'mv {self.backup_path} {self.file_path}')

    def verify_and_rollback(self):
        __xpr('Running verification...')
        if os.system(self.verify_command):
            __xpr('Verification failed! Restoring original config...')
            self.restore()
            __xpr('Original config restored.')
        else:
            __xpr('Verification successful.')