import json
import urllib.request
import re
import shutil
import os
import zipfile
import tarfile
import requests


def fetch_cs_sharp():
    _json = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://api.github.com/repos/roflmuffin/CounterStrikeSharp/releases/latest',
        headers={'Accept': 'application/vnd.github.v3+json'},
    )).read())
    for asset in _json['assets']:
        if re.search("counterstrikesharp-build-.*-linux-.*.zip", asset["name"]):
            urllib.request.urlretrieve(asset['browser_download_url'], filename="temp/counterstrikesharp-latest.zip")


def fetch_metamod():
    r = requests.get('https://www.sourcemm.net/downloads.php/?branch=master')
    test = r.text.split("<div style=")
    find = "quick-download download-link.*https://mms.alliedmods.net.*-linux.tar.gz"
    for line in test:
        if re.search(find, line):
            url = line[line.find("https:"):(line.find(".gz")+3)]
            with open('temp/metamod-latest.tar.gz', 'wb') as out_file:
                content = requests.get(url, stream=True).content
                out_file.write(content)


def unzip(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall("temp/game/csgo")
    os.remove(f"{file}")


def extract_tar(file):
    tarfile.open(file).extractall("temp/game/csgo")
    os.remove(f"{file}")


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.sep)


shutil.copytree("source", "temp")

fetch_cs_sharp()
unzip("temp/counterstrikesharp-latest.zip")
fetch_metamod()
extract_tar("temp/metamod-latest.tar.gz")
make_tarfile("//192.168.1.2/server/opt/fileserver/CS2_server_config/10man_test/cs2_cfg.gz", "temp")

shutil.rmtree("temp")
