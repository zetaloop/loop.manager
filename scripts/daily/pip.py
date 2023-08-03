# Python pip packages update

print('Checking pip outdated...')
import subprocess, json, os
pipcmd = ["pip", "list", "--outdated", "--format", "json"]
jsondata = json.loads(subprocess.run(pipcmd, capture_output=True, text=True).stdout)
allpackages = [pkg['name'] for pkg in jsondata]

print('-' * 16)
if not jsondata:
    print('(No update)')
for i in jsondata:
    print(f"{i['name']} {i['version']} >>> {i['latest_version']}")
print('-' * 16)

packages = allpackages
errorpackages = []
while packages:
    print('Try updating: ' + ' '.join(packages))
    if os.system('pip install -U ' + ' '.join(packages)):
        print('An error has occurred, checking...')
        pipcmd = 'pip install -U'.split() + packages
        result = subprocess.run(pipcmd, capture_output=True, text=True).stdout
        err_lines = [i for i in result.split('\n') if i.startswith('Collecting')]
        if err_lines:
            err_line_parts = err_lines[-1].split(' ')
            if err_line_parts:
                err = err_line_parts[1]
                errorpackages.append(err)
                print('Try ignoring package: ' + ' '.join(errorpackages))
                erri = packages.index(err)
                print('And updating: ' + ' '.join(packages[:erri]))
                if os.system('pip install -U ' + ' '.join(packages[:erri])):
                    print('Another error has occured. Please solve the problem manually. Auto update stopped.')
                    exit()
                packages = packages[erri + 1:]
    else:
        break

installedpackages = [i for i in allpackages if i not in errorpackages]
print(f'Update finished {len(installedpackages)}/{len(allpackages)}')
print('Updated: ' + ' '.join(installedpackages))
print('Ignored: ' + ' '.join(errorpackages))
