from bx_py_utils.test_utils.context_managers import MassContextManager
from manageprojects.test_utils.click_cli_utils import subprocess_cli

from ha_services.cli_tools.test_utils.mock_rich import NoColors
from ha_services.toml_settings.test_utils.data_class_utils import MockTomlSettings


class CliMock(MassContextManager):
    """
    IMPORTANT: We must ensure that no local user settings added to the help text
    So we can't directly invoke_click() here, because user settings are read and
    used on module level!
    So we must use subprocess and use a default settings file!
    """

    def __init__(
        self,
        *,
        SettingsDataclass,
        settings_overwrites: dict,  # Change values in SettingsDataclass instance
        dir_name='mocked_dir_name',
        file_name='mocked_file_name',
        prefix='test_mock',  # Temp dir prefix
    ):
        self.mocks = (
            MockTomlSettings(
                SettingsDataclass=SettingsDataclass,
                settings_overwrites=settings_overwrites,
                dir_name=dir_name,
                file_name=file_name,
                prefix=prefix,
            ),
            NoColors(),
        )

    def invoke(self, *, cli_bin, args) -> str:
        stdout = subprocess_cli(cli_bin=cli_bin, args=args)

        # Skip header stuff:
        lines = stdout.splitlines()
        found = False
        for pos, line in enumerate(lines):
            if line.lstrip().startswith('Usage: '):
                stdout = '\n'.join(lines[pos:])
                found = True
                break

        assert found is True, f'Usage line not found in: {stdout!r}'

        return '\n'.join(line.rstrip() for line in stdout.splitlines())
