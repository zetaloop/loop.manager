import os
import subprocess

VERSION = '1.0'

def scan_dir(directory):
    subdirs = []
    for i in os.listdir(directory):
        ipath = os.path.join(directory, i)
        if os.path.isdir(ipath):
            subdirs.append(i)
    return sorted(subdirs)

def scan_script(directory):
    scripts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sh') or file.endswith('.py'):
                scripts.append(os.path.join(root, file))
    return sorted(scripts)

def execute_script(script_path):
    if script_path.endswith('.py'):
        env = os.environ.copy()
        env['PYTHONPATH'] = '.'
        subprocess.run(['python3', script_path], check=True, env=env)
    elif script_path.endswith('.sh'):
        subprocess.run(['bash', script_path], check=True)

def cdself():
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    os.chdir(script_dir)

def ln(path):
    with open(path) as f:
        commentln = f.readline().strip()
        if commentln.startswith('#'):
            return '\n ' + commentln
        else:
            return ''

def main():
    print('\n' + '=' * 16 + f'[Loop Manager v{VERSION}]' + '=' * 16)
    cdself()
    catagories = scan_dir('scripts')
    print('\n'.join(f'{index}: {cat}' for index, cat in enumerate(catagories)))
    try:
        catagory = catagories[int(input('[Catagory?] '))]
        print()
    except:
        print('No.Exit.')
    scripts = scan_script(os.path.join('scripts', catagory))
    print('\n'.join(f'{index}: {os.path.split(path)[1]}{ln(path)}' for index, path in enumerate(scripts)) if scripts else '(None)')
    try:
        script = scripts[int(input('[Script?] '))]
        print()
    except:
        print('No.Exit.')
        exit()
    print('>>> ' + script)
    execute_script(script)
    print('=' * 16 + '[Loop Manager Execution Over]' + '=' * 16)

if __name__ == '__main__':
    main()
