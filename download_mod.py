import json
import requests
import glob
import hashlib

RELATIVE_MOD_PATH = 'Factorio/mods/'
USERNAME = 'username'
TOKEN = 'token'


def has_downloaded(mod_name):
    if mod_name == 'base':
        return True

    filenames = glob.glob(f"{RELATIVE_MOD_PATH}{mod_name}_*.zip")
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


def download_mod(mod_name):
    url = f"https://mods.factorio.com/api/mods/{mod_name}"
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        json_object = json.loads(r.text)
        download_file(json_object['releases'][-1])
    else:
        print(f"Unable to download mod info: {mod_name}")


def download_mods():
    with open(f"{RELATIVE_MOD_PATH}mod-list.json") as json_string:
        json_obj = json.load(json_string)
        for mods in json_obj['mods']:
            if not has_downloaded(mods['name']) and mods['enabled']:
                download_mod(mods['name'])


if __name__ == '__main__':
    download_mods()
