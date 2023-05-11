import logging
from pathlib import Path

from ha_services.cli_tools.path_utils import expand_user


logger = logging.getLogger(__name__)


def clean_settings_path(settings_path: str) -> Path:
    settings_path = expand_user(Path(settings_path))  # Expand with user home, even if called via sudo!

    assert settings_path.suffix == '.toml', f'File extension must be ".toml": {settings_path=}'
    return settings_path
