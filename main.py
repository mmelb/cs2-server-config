import json
import urllib.request
import re

_json = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://api.github.com/repos/roflmuffin/CounterStrikeSharp/releases/latest',
     headers={'Accept': 'application/vnd.github.v3+json'},
)).read())
for asset in _json['assets']:
    if re.search("counterstrikesharp-build-.*-linux-.*.zip", asset["name"]):
        urllib.request.urlretrieve(asset['browser_download_url'], asset['name'])
        print(f"downloading {asset['name']}")
