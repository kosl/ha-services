import getpass
import logging
import os
import pwd
import shutil
from pathlib import Path

from bx_py_utils.environ import OverrideEnviron
from bx_py_utils.path import assert_is_file


logger = logging.getLogger(__name__)


def expand_user(path: Path) -> Path:
    """
    Returns a new path with expanded ~ and ~user constructs:
    Unlike the normal Python function, when called with sudo, the normal user path is used.
    So "~" is not expanded as "/root" -> it's expanded with the user home that sudo starts with!
    """

    if sudo_user := os.environ.get('SUDO_USER'):
        env_user = getpass.getuser()
        if sudo_user != env_user:
            # Get home directory of the user that starts sudo via password database:
            sudo_user_home = pwd.getpwnam(sudo_user).pw_dir
            with OverrideEnviron(HOME=sudo_user_home):
                return Path(path).expanduser()
    else:
        return Path(path).expanduser()


def backup(file_path: Path, max_try=100) -> Path:
    """
    Backup the given file, by create copy with the suffix: ".bak"
    Increment a number to the suffix -> So no old backup file will be overwritten.
    """
    assert_is_file(file_path)
    for number in range(1, max_try + 1):
        bak_file_candidate = file_path.with_name(f'{file_path.name}.bak{number if number>1 else ""}')
        if not bak_file_candidate.is_file():
            logger.info('Backup %s to %s', file_path, bak_file_candidate)
            shutil.copyfile(file_path, bak_file_candidate)
            return bak_file_candidate
    raise RuntimeError('No backup made: Maximum attempts to find a file name failed.')
