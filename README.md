# factorio_mod_downloader

This script is for downloading enabled mods from mods/mod-list.json.  It's ideal for debugging mods compatibility crashes on data stage.  Especially someone enable your mod and crash immediately.  They would not have a save to sync.

### Use in Factorio's root folder
1. Copy download_mod.py to Factorio's root.
2. Open the file to add your factorio.com USERNAME and TOKEN. The token can be found in https://factorio.com/profile 
3. Run "python download_mod.py"

### Use outside Factorio's root folder
1. Open the file to change RELATIVE_MOD_PATH.
2. Add your factorio.com USERNAME and TOKEN. The token can be found in https://factorio.com/profile 
3. Run "python download_mod.py"
