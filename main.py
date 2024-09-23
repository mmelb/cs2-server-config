import json
import urllib.request
import re
import tarfile
import shutil
import os
import zipfile


def fetch_cs_sharp():
    _json = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://api.github.com/repos/roflmuffin/CounterStrikeSharp/releases/latest',
        headers={'Accept': 'application/vnd.github.v3+json'},
    )).read())
    for asset in _json['assets']:
        if re.search("counterstrikesharp-build-.*-linux-.*.zip", asset["name"]):
            urllib.request.urlretrieve(asset['browser_download_url'], filename="temp/counterstrikesharp-latest.zip")


def unzip():
    with zipfile.ZipFile("temp/counterstrikesharp-latest.zip", 'r') as zip_ref:
        zip_ref.extractall("temp/game/csgo")
    os.remove("temp/counterstrikesharp-latest.zip")


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.sep)


shutil.copytree("source", "temp")

fetch_cs_sharp()
unzip()
make_tarfile("//192.168.1.2/server/opt/fileserver/CS2_server_config/10man_test/cs2_cfg.gz", "temp")

shutil.rmtree("temp")
