import os
import subprocess
import conf

VERSION = '1.0'

def scan_subdirectories(directory):
    subdirectories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subdirectories.append(item)
    return subdirectories

def scan_scripts(directory):
    scripts = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.sh') or file.endswith('.py'):
                scripts.append(os.path.join(root, file))
    return scripts

def execute_script(script_path):
    if script_path.endswith('.py'):
        host = 'python3'
    elif script_path.endswith('.sh'):
        host = 'bash'
    subprocess.run([host, script_path], check=True)

def change_to_script_directory():
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
    last = conf.get('last', None)
    print('Last use:', last, '\n')
    change_to_script_directory()
    catagories = scan_subdirectories('scripts')
    print('\n'.join(f'{index}: {cat}' for index, cat in enumerate(catagories)))
    try:
        catagory = catagories[int(input('[Catagory?] '))]
        print()
    except:
        print('No.Exit.')
    scripts = scan_scripts(os.path.join('scripts', catagory))
    print('\n'.join(f'{index}: {os.path.split(path)[1]}{ln(path)}' for index, path in enumerate(scripts)) if scripts else '(None)')
    try:
        script = scripts[int(input('[Script?] '))]
        print()
    except:
        print('No.Exit.')
        exit()
    print('>>> ' + script)
    conf.data['last'] = catagory + '/' + os.path.split(script)[1]
    conf.save()
    execute_script(script)
    print('=' * 16 + '[Loop Manager Execution Over]' + '=' * 16)

if __name__ == '__main__':
    main()
