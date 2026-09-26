#!/usr/bin/env python3
"""Fetch public CS:GO query results for GitHub Pages; no credentials needed."""
import datetime, json, pathlib, urllib.request

SERVERS = {1: ('168.100.161.99', 2462), 2: ('168.100.161.119', 27065)}
DATA = pathlib.Path(__file__).resolve().parents[1] / 'data'
DATA.mkdir(exist_ok=True)

for number, (ip, port) in SERVERS.items():
    destination = DATA / f'server{number}.json'
    url = f'https://gamedig-api.hexane.co/csgo/ip={ip}&port={port}'
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'PicklesCommunityStatus/1.0', 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=22) as response:
            result = json.load(response)
        if result.get('online') is not True:
            raise ValueError('API did not report the server as online')
        players = result.get('players') if isinstance(result.get('players'), list) else []
        raw = result.get('raw') if isinstance(result.get('raw'), dict) else {}
        output = {
            'online': True,
            'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'name': result.get('name', ''),
            'map': result.get('map', ''),
            'numplayers': raw.get('numplayers', len(players)),
            'maxplayers': result.get('maxplayers'),
            'players': [{'name': p.get('name', ''), 'score': p.get('raw', {}).get('score') if isinstance(p.get('raw'), dict) else None} for p in players if isinstance(p, dict)]
        }
        destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'Server {number}: updated successfully')
    except Exception as exc:
        # Preserve last good result; website will label it outdated based on checked_at.
        print(f'Server {number}: update failed: {exc}')
        if not destination.exists():
            destination.write_text(json.dumps({'online': False, 'error': 'First successful update pending'}, indent=2) + '\n')
