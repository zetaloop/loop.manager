# Python pip packs update

print('Updating pip...')
import subprocess, json, os
os.system('python3 -m pip install -U pip')

print('Checking pip outdated...')
pipcmd = ["pip", "list", "--outdated", "--format", "json"]
jsondata = json.loads(subprocess.run(pipcmd, capture_output=True, text=True).stdout)
allpacks = [pkg['name'] for pkg in jsondata]

print('-' * 16)
if not jsondata:
    print('(No update)')
for i in jsondata:
    print(f"{i['name']} {i['version']} >>> {i['latest_version']}")
print('-' * 16)

packs = allpacks
error_packs = []

def errorhandler(error_pack):
    global packs
    error = packs.index(err)
    print('Try ignoring pack: ' + ' '.join(error_pack))
    error_packs.append(error_pack)
    mainloop(packs[:error])
    packs = packs[error + 1:]

def check(result):
    packs = [i for i in result if i.startswith('Collecting')]
    if not packs:
        print('Unexpected error!')
        exit()
    error_pack = packs[-1].split(' ')[1]
    if [i for i in result if i.startswith('ERROR: Cannot uninstall')]:
        print('Uninstall failed, try force install: ' + error_pack)
        if not os.system('pip install -U --ignore-installed ' + error_pack):
            return
    errorhandler(error_pack)

def mainloop(packs):
    print('Try updating: ' + ' '.join(packs))
    if os.system('pip install -U ' + ' '.join(packs)):
        print('An error has occurred, checking...')
        pipcmd = 'pip install -U'.split() + packs
        result = subprocess.run(pipcmd, capture_output=True, text=True).stdout.split('\n')
        check(result)
    else:
        packs.clear()

while packs:
    mainloop(packs)

installed_packs = [i for i in allpacks if i not in error_packs]
print(f'Update finished {len(installed_packs)}/{len(allpacks)}')
print('Updated: ' + ' '.join(installed_packs))
print('Ignored: ' + ' '.join(error_packs))
