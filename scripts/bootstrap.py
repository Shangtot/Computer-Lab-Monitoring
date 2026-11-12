from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ensure_directories() -> None:
    directories = [
        ROOT / 'backend' / 'app' / 'models',
        ROOT / 'backend' / 'app' / 'schemas',
        ROOT / 'backend' / 'app' / 'routes',
        ROOT / 'backend' / 'app' / 'services',
        ROOT / 'backend' / 'app' / 'authentication',
        ROOT / 'backend' / 'app' / 'utils',
        ROOT / 'agent',
        ROOT / 'browser-extension',
        ROOT / 'frontend' / 'css',
        ROOT / 'frontend' / 'js',
        ROOT / 'database',
        ROOT / 'network',
        ROOT / 'tests',
        ROOT / 'docs',
        ROOT / 'scripts',
        ROOT / 'data',
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    ensure_directories()
    print('Project structure validated.')
