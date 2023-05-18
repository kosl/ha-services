import tempfile
from pathlib import Path
from unittest import TestCase

from ha_services.example import SystemdServiceInfo
from ha_services.systemd.test_utils.mock_systemd_info import MockSystemdServiceInfo


class SystemdDataClassesTestCase(TestCase):
    def test_systemd_service_info(self):
        info = SystemdServiceInfo()

        # Check some samples:
        self.assertEqual(info.template_context.verbose_service_name, 'HaServices Demo')
        self.assertEqual(info.service_slug, 'haservices_demo')
        self.assertEqual(info.template_context.syslog_identifier, 'haservices_demo')
        self.assertEqual(info.service_file_path, Path('/etc/systemd/system/haservices_demo.service'))

        with MockSystemdServiceInfo(
            prefix='test_systemd_service_info_', SystemdServiceInfoClass=SystemdServiceInfo
        ) as cm:
            info = cm.systemd_info

            self.assertIsInstance(info, SystemdServiceInfo)
            self.assertEqual(info.template_context.user, 'MockedUserName')
            self.assertEqual(info.template_context.group, 'MockedUserName')
            self.assertEqual(
                info.template_context.exec_start, '/mocked/.venv/bin/python3 -m ha_services_app publish-loop'
            )

            base_temp_dir = tempfile.gettempdir()
            assert str(info.template_context.work_dir).startswith(
                base_temp_dir
            ), f'{info.template_context.work_dir} does not start with {base_temp_dir}'