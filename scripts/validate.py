#!/usr/bin/env python3
"""Validate public-package boundaries and marketplace/component consistency."""
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def main():
    marketplace = read(ROOT / '.agents/plugins/marketplace.json')
    inventory = read(ROOT / 'catalog.json')
    assert marketplace['name'] == 'emory-mcp'
    endpoints = {entry['plugin']: entry['url'] for entry in inventory['endpoints']}
    assert len(endpoints) == len(marketplace['plugins']) == 2
    paths = []
    for entry in marketplace['plugins']:
        assert entry['policy'] == {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}
        source = entry['source']
        assert source['source'] == 'local' and source['path'].startswith('./plugins/')
        folder = (ROOT / source['path']).resolve()
        assert folder.is_relative_to(ROOT) and folder.is_dir()
        manifest = read(folder / 'plugin.json')
        compat = read(folder / '.codex-plugin/plugin.json')
        assert manifest['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
        assert manifest['name'] == compat['name'] == entry['name'] == folder.name
        assert manifest['version'] == compat['version']
        assert re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', manifest['version'])
        extension = manifest['extensions']['com.openai']
        assert extension['interface'] == compat['interface']
        assert len(extension['interface']['shortDescription']) <= 30
        assert compat['mcpServers'] == './.mcp.json'
        assert 'skills' not in compat and 'onboardingSkill' not in extension
        assert not folder.joinpath('skills').exists()
        assert not list(folder.rglob('SKILL.md'))
        assert not any('onboardingSkill' in e for e in compat.get('extensions', {}).values())
        connection = read(folder / 'mcp.json')
        assert connection['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
        assert set(connection['mcpServers']) == {'platform'}
        server = connection['mcpServers']['platform']
        assert set(server) == {'type', 'url'}
        assert server['type'] == 'streamable-http'
        legacy = read(folder / '.mcp.json')
        assert legacy == {'mcpServers': {'platform': {'type': 'http', 'url': server['url']}}}
        assert server['url'] == endpoints[entry['name']]
        url = urlsplit(server['url'])
        assert url.scheme == 'https' and url.netloc == 'mcphub.int.emory.edu'
        assert not url.username and not url.password and not url.query and not url.fragment
        access = entry['name'].removeprefix('emory-platform-')
        assert access in {'readonly', 'full'} and url.path == '/mcp/platform-official-' + access
        assert not any(k in server for k in ('headers', 'http_headers', 'bearer_token_env_var', 'oauth'))
        paths.append(url.path)
    assert len(set(paths)) == 2
    for path in ROOT.rglob('*'):
        if '.git' in path.parts:
            continue
        assert not path.is_symlink(), 'Public package may not contain symlinks'
        if not path.is_file():
            continue
        assert path.name not in {'.env', '.app.json', 'config.toml', 'mcp_settings.json'}
        text = path.read_text()
        assert not re.search(r'-----BEGIN (?:[A-Z ]*PRIVATE KEY)-----', text)
        assert not re.search(r'\b(?:ghp_|github_pat_|mcphub_)[A-Za-z0-9_]{20,}', text)
        assert not re.search(r'[A-Za-z0-9._%+-]+@emory\.edu', text), 'No user roster in public source'
    print('PASS: two OAuth-discovered group definitions, contained sources, synchronized versions/metadata, no bundled/automatic setup skills and public-package boundaries')


if __name__ == '__main__':
    main()
