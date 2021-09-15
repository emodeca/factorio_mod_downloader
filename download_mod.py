import json
import requests
import glob
import hashlib

RELATIVE_MOD_PATH = 'mods/'
USERNAME = 'username'
TOKEN = 'token'


def has_downloaded(mod):
    if mod['name'] == 'base':
        return True

    if 'version' in mod:
        filenames = glob.glob(f"{RELATIVE_MOD_PATH}{mod['name']}_{mod['version']}.zip")
    else:
        filenames = glob.glob(f"{RELATIVE_MOD_PATH}{mod['name']}_*.zip")

    if len(filenames):
        return True

    return False


def download_file(download_obj):
    url = f"https://mods.factorio.com{download_obj['download_url']}?username={USERNAME}&token={TOKEN}"
    r = requests.get(url, allow_redirects=True)
    sha1 = hashlib.sha1()
    sha1.update(r.content)
    if sha1.hexdigest() == download_obj['sha1']:
        open(f"{RELATIVE_MOD_PATH}{download_obj['file_name']}", 'wb').write(r.content)
        print(f"Downloaded {download_obj['file_name']}")
    else:
        print(f"Download Failed {download_obj['file_name']}")


def download_mod(mod):
    url = f"https://mods.factorio.com/api/mods/{mod['name']}"
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        json_object = json.loads(r.text)
        if 'version' in mod:
            for release in json_object['releases']:
                if release['version'] == mod['version']:
                    download_file(release)
        else:
            download_file(json_object['releases'][-1])

    else:
        print(f"Unable to download mod info: {mod['name']}")


def download_mods():
    with open(f"{RELATIVE_MOD_PATH}mod-list.json") as json_string:
        json_obj = json.load(json_string)
        for mod in json_obj['mods']:
            if mod['enabled'] and not has_downloaded(mod):
                download_mod(mod)


if __name__ == '__main__':
    download_mods()
